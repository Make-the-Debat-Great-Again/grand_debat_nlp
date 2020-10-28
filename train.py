# -*- coding: utf-8 -*-

import os
import argparse

# BASIC
import pandas as pd
import numpy as np

#NLP
from stop_words import get_stop_words
from keras.preprocessing.text import Tokenizer
from lib.utils import lemmatize

# ML
# MACHINE LEARNING
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC
from sklearn.linear_model import SGDClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier

from sklearn.model_selection import GridSearchCV

# ML HELPERS
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

#PROGRESS BAR
from tqdm import tqdm

import joblib

# CUSTOM
from lib.constant import *


classifier_dict = {
    "naive-bayes":MultinomialNB(),
    "svm":SVC(kernel="rbf"),
    "sgd":SGDClassifier(),
    "knn":KNeighborsClassifier(),
    "decision-tree": DecisionTreeClassifier(),
    "random-forest":RandomForestClassifier()
}

parameters = {
    "naive-bayes":[{"alpha":[0,1]}],
    "svm":[{"kernel":["rbf","poly"], 'gamma': [1e-1,1e-2,1e-3, 1,10,100]}],
    "sgd":[{"penalty":["l1","l2"],"loss":["hinge","modified_huber","log"]}],
    "knn":[{"n_neighbors":list(range(4,8)),"p":[1,2]}],
    "decision-tree": [{"criterion":["gini","entropy"]}],
    "random-forest":[{"criterion":["gini","entropy"],"n_estimators":[10,50,100]}]
}


parser = argparse.ArgumentParser()
parser.add_argument("data_transition_eco_fn",help="Official CSV file for the Transition Ecologique")#,default="data/LA_TRANSITION_ECOLOGIQUE.csv")
parser.add_argument("data_annotation_fn",help="Official CSV from the Grande Annotation")#,default="data/results.csv")
parser.add_argument("-o",action="store_true",help="Directly train the model with optimal parameter")
parser.add_argument("-s",action="store_true",help="Use Spacy")

args = parser.parse_args()
print(args)

if not os.path.exists(args.data_transition_eco_fn):
    raise FileNotFoundError("File {0} was not found !".format(args.data_transition_eco_fn))

if not os.path.exists(args.data_annotation_fn):
    raise FileNotFoundError("File {0} was not found !".format(args.data_annotation_fn))

########################################################################################
##################################### READ DATA ########################################
########################################################################################

# READ THE DATA
df = pd.read_csv(args.data_transition_eco_fn)
df.rename(columns=question_code,inplace=True) # On renomme les colonnes
df.fillna("",inplace=True) # On remplace les valeurs nulles par une chaine de caractères vide

# READ ANNOTATION DATA
df_annotation = pd.read_csv(args.data_annotation_fn) # Chargement des données de la Grande annotation


data = {} # On récupère les données textuelles (réponses)
for _,row in tqdm(df.iterrows(),total=len(df)):
    data[row.reference]={}
    for q in question_ids:
        if not row[q]=="":
            data[row.reference][q]=row[q]

# On associe le texte de la réponse pour chaque enregistrement de la grande annotations 
df_annotation["text"] = df_annotation.apply(\
                                            lambda x: data[x.Contribution][x.Question] \
                                                if (x.Contribution in data and x.Question in data[x.Contribution])\
                                                else "",axis=1)

df_annotation = df_annotation[df_annotation.text.apply(lambda x:len(x)>0) ][df_annotation.Question.isin(question_ids)]
df_annotation["is_transport"] = df_annotation.Categorie.isin(transport_cat).astype(int) # A l'aide des catégories ci-dessus, on indique quelle réponse parle de transport
df_annotation_transport = df_annotation.drop_duplicates("Contribution")
df_annotation["weight"] = df_annotation.text.apply(len)



########################################################################################
################################## BUILD DATASET #######################################
########################################################################################

class_non_transport = df_annotation[df_annotation.is_transport == 0].sample(frac=0.15,weights="weight") # On récupère des réponses qui n'ont rien avoir avec le transport
class_transport = df_annotation[df_annotation.is_transport == 1].sample(frac=1)

dataset = pd.concat((class_non_transport,class_transport)) # On construit le jeu de données final

########################################################################################
###########################BUILD TRAINING/TESTING DATASET ##############################
########################################################################################


# EXTRACT LEMMATIZED FORM FROM INPUT TEXTS
fr_stop = get_stop_words("french")


## EXTRACT LEMMATIZED VERSION OF INPUT TEXTS
#TALISMANE
if not args.s:
    dataset["lemma"] = lemmatize(dataset.text.values,fr_stop,lemmatizer="talismane")
    dataset["lemma"] = dataset.lemma.apply(lambda x:" ".join(x))
#SPACY
else:
    dataset["lemma"] = lemmatize(dataset.text.values,fr_stop)

# SPLIT DATASET INTO TRAIN AND TEST
X,y = [" ".join(x) for x in dataset.lemma.values],dataset.is_transport.values


data_vectorizer = Pipeline([
    ('vect', CountVectorizer()),
    ('tfidf', TfidfTransformer()),
])
data_vectorizer.fit(X)
X_train,X_test,y_train,y_test = train_test_split(X,y)
X_train = data_vectorizer.transform(X_train)
X_test = data_vectorizer.transform(X_test)

########################################################################################
################################### TRAIN THE MODEL ####################################
########################################################################################
print("Train Classifier...")

if args.o: # train the model using optimal parameters
    clf = MultinomialNB(alpha=1)
    clf.fit(X_train, y_train)
    joblib.dump(clf,filename="resources/classification_model/classifier_multinomialnb.dump")
    joblib.dump(data_vectorizer,filename="resources/classification_model/vectorizer.dump")
else:
    for CLASSIFIER in classifier_dict:
        print("TRAIN AND EVAL {0}".format(CLASSIFIER))
        clf = GridSearchCV(
                classifier_dict[CLASSIFIER], parameters[CLASSIFIER], scoring='f1_weighted',n_jobs=-1
            )
        clf.fit(X_train, y_train)
        print("Best Parameters : ",clf.best_params_)
        y_pred = clf.best_estimator_.predict(X_test)
        print(classification_report(y_test,y_pred))






# TRAIN AND EVAL naive-bayes
# Best Parameters :  {'alpha': 1}
#               precision    recall  f1-score   support

#            0       0.83      0.92      0.88      1752
#            1       0.91      0.80      0.85      1655

#     accuracy                           0.87      3407
#    macro avg       0.87      0.86      0.86      3407
# weighted avg       0.87      0.87      0.86      3407

# TRAIN AND EVAL svm
# Best Parameters :  {'gamma': 0.1, 'kernel': 'rbf'}
#               precision    recall  f1-score   support

#            0       0.82      0.92      0.87      1752
#            1       0.90      0.79      0.84      1655

#     accuracy                           0.86      3407
#    macro avg       0.86      0.85      0.85      3407
# weighted avg       0.86      0.86      0.85      3407

# TRAIN AND EVAL sgd
# Best Parameters :  {'loss': 'log', 'penalty': 'l1'}
#               precision    recall  f1-score   support

#            0       0.84      0.90      0.87      1752
#            1       0.89      0.82      0.85      1655

#     accuracy                           0.86      3407
#    macro avg       0.87      0.86      0.86      3407
# weighted avg       0.86      0.86      0.86      3407

# TRAIN AND EVAL knn
# Best Parameters :  {'n_neighbors': 5, 'p': 2}
#               precision    recall  f1-score   support

#            0       0.69      0.99      0.81      1752
#            1       0.97      0.53      0.68      1655

#     accuracy                           0.76      3407
#    macro avg       0.83      0.76      0.75      3407
# weighted avg       0.83      0.76      0.75      3407

# TRAIN AND EVAL decision-tree
# Best Parameters :  {'criterion': 'gini'}
#               precision    recall  f1-score   support

#            0       0.81      0.88      0.84      1752
#            1       0.86      0.78      0.82      1655

#     accuracy                           0.83      3407
#    macro avg       0.84      0.83      0.83      3407
# weighted avg       0.84      0.83      0.83      3407

# TRAIN AND EVAL random-forest
# Best Parameters :  {'criterion': 'entropy', 'n_estimators': 100}
#               precision    recall  f1-score   support

#            0       0.82      0.88      0.85      1752
#            1       0.86      0.80      0.83      1655

#     accuracy                           0.84      3407
#    macro avg       0.84      0.84      0.84      3407
# weighted avg       0.84      0.84      0.84      3407
