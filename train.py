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
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report

#PROGRESS BAR
from tqdm import tqdm

import joblib

# CUSTOM
from lib.constant import *

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
X,y = dataset.lemma.values,dataset.is_transport.values
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42) # Split train/test

# BUILD A TOKENIZER
max_words = 10000
tokenizer = Tokenizer(num_words=max_words)
tokenizer.fit_on_texts(np.concatenate((X_train,X_test)))

# PARSE INPUT TEXT TO BAGOFWORDS REPRESENTATION
X_train = tokenizer.texts_to_sequences(X_train)
X_test = tokenizer.texts_to_sequences(X_test)
X_train = tokenizer.sequences_to_matrix(X_train, mode='binary')
X_test = tokenizer.sequences_to_matrix(X_test, mode='binary')



########################################################################################
################################### TRAIN THE MODEL ####################################
########################################################################################
print("Train Classifier...")
if args.o: # train the model using optimal parameters
    clf = svm.SVC(gamma=0.01,kernel="rbf")
    clf.fit(X_train, y_train)
    joblib.dump(clf,filename="resources/classification_model/classifier_svm.dump")
    joblib.dump(tokenizer,filename="resources/classification_model/tokenizer.dump")

else:
    tuned_parameters = [{'kernel': ['rbf'], 'gamma': [1e-1,1e-2,1e-3, 1,10,100]}]
    clf = GridSearchCV(
            svm.SVC(), tuned_parameters, scoring='f1',verbose=10,n_jobs=-1
        )
    clf.fit(X_train, y_train)

    print("Best parameters set found on development set:")
    print()
    print(clf.best_params_)
    print()
    print("Grid scores on development set:")
    print()
    means = clf.cv_results_['mean_test_score']
    stds = clf.cv_results_['std_test_score']
    for mean, std, params in zip(means, stds, clf.cv_results_['params']):
        print("%0.3f (+/-%0.03f) for %r"
                % (mean, std * 2, params))
    print()

    print("Detailed classification report:")
    print()
    print("The model is trained on the full development set.")
    print("The scores are computed on the full evaluation set.")
    print()
    y_true, y_pred = y_test, clf.predict(X_test)
    print(classification_report(y_true, y_pred))


    ########################################################################################
    #################################### SAVE THE MODEL ####################################
    ########################################################################################

    joblib.dump(clf.best_estimator_,filename="resources/classification_model/classifier_svm.dump")
    joblib.dump(tokenizer,filename="resources/classification_model/tokenizer.dump")


# RESULTS
# Best parameters set found on development set:

# {'gamma': 0.01, 'kernel': 'rbf'}

# Grid scores on development set:

# 0.820 (+/-0.013) for {'gamma': 0.1, 'kernel': 'rbf'}
# 0.830 (+/-0.013) for {'gamma': 0.01, 'kernel': 'rbf'}
# 0.768 (+/-0.035) for {'gamma': 0.001, 'kernel': 'rbf'}
# 0.650 (+/-0.036) for {'gamma': 1, 'kernel': 'rbf'}
# 0.549 (+/-0.032) for {'gamma': 10, 'kernel': 'rbf'}
# 0.549 (+/-0.032) for {'gamma': 100, 'kernel': 'rbf'}

# Detailed classification report:

# The model is trained on the full development set.
# The scores are computed on the full evaluation set.