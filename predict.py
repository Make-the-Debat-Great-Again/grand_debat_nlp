
import pandas as pd

import json
import numpy as np
from tqdm import tqdm
tqdm.pandas()
import argparse
import joblib

from lib.utils import parallel_talismane,extract_lemma_spacy
import spacy


import nltk
from nltk.tokenize import word_tokenize

from joblib import Parallel,delayed

question_col_index_to_analyse = {
    "transition_eco":[0,1,3,5,6,7,9,11,12,13,14,15],
    "democratie_et_citoy":[0,2,3,4,5,6,8,9,11,12,14,15,16,18,19,20,21,22,23,24,25,26,27,28,29,31,32,34,35,36],
    "fiscalite_et_depense_publique":[0,1,2,3,4,5,6,7],
    "organisation_de_etat_et_service_pub":[0,2,3,4,5,7,8,9,10,12,13,14,16,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32]
}

code_questions = {
    1:"transition_eco",
    2:"democratie_et_citoy",
    3:"fiscalite_et_depense_publique",
    4:"organisation_de_etat_et_service_pub"
}


parser = argparse.ArgumentParser()

parser.add_argument("input_dataset")
parser.add_argument("code_dataset",type=int,help=";".join(["{0} - {1} ".format(k,v)for k,v in code_questions.items()]))
parser.add_argument("-s",action="store_true",help="Use Spacy to lemmatize")

args = parser.parse_args()#("LA_TRANSITION_ECOLOGIQUE.csv 1".split())

# LOAD DATA
df = pd.read_csv(args.input_dataset,dtype={"authorZipCode":str}).fillna("J'aime le paté.")
QUESTIONS_INDEXES = question_col_index_to_analyse[code_questions[args.code_dataset]]


# LOAD CLASSIFIER
clf = joblib.load("./resources/classification_model/classifier_svm.dump")
tokenizer = joblib.load("./resources/classification_model/tokenizer.dump")

def classify(x):
    if len(x)<1:
        return 0
    #print(x)
    x = tokenizer.sequences_to_matrix(
        tokenizer.texts_to_sequences(
            [" ".join(x)])
        ,mode = "binary")
    return clf.predict(x)[0]

reponse_columns = df.columns[11:]

def transform_and_return(df):
    df.LEMMA = df.apply(lambda x : str(x.FORM).lower() if str(x.LEMMA)=="_" else str(x.LEMMA),axis=1)
    return df

new_data = {}
if args.s:
    nlp = spacy.load("fr")

for x in QUESTIONS_INDEXES:
    col = reponse_columns[x]
    print("Process the question:",col)
    print("Lemmatisation...")
    if not args.s:
        lemma = [transform_and_return(talismane_data).LEMMA.values for talismane_data in parallel_talismane(data=df[col].values,batch_size=1000)]
    else:
        extract_lemma_spacy(nlp,df,col,stop_words=[])
        lemma = df["lemma"].values
    print("Classification...")
    new_data[col] = Parallel(n_jobs=-1,backend="multiprocessing")(delayed(classify)(x) for x in tqdm(lemma)) 

new_data["publishedAt"] = df.publishedAt
new_data["reference"] = df.reference.values
new_data["authorId"] = df.authorId
new_data["authorZipCode"] = df.authorZipCode


pd.DataFrame.from_dict(new_data).to_csv("{0}.csv".format(code_questions[args.code_dataset]),sep="\t",index=False)

print("Results can be found in the following file :","{0}.csv".format(code_questions[args.code_dataset]))