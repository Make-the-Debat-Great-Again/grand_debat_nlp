#!/usr/bin/env python
# coding: utf-8
import os
import argparse
import json

# Custom library
from lib.textometry import *
from lib.helpers import *
from lib.constant import *


from lib.utils import lemmatize
from stop_words import get_stop_words
fr_stop = get_stop_words("french")


# Pandas shoots warning non-stop ... so chouh !
import warnings
warnings.simplefilter(action='ignore', category=pd.errors.DtypeWarning)

parser = argparse.ArgumentParser()
parser.add_argument("data_fn")
parser.add_argument("classification_result_fn")
parser.add_argument("-s",action="store_true",help="Use Spacy to lemmatize")


args = parser.parse_args()

for fn in [args.classification_result_fn, args.data_fn]:
    if not os.path.exists(fn):
        raise FileNotFoundError("File {0} was not found !".format(fn))

##### LOAD ANNOTATION AND ORIGINAL DATASET
df_classification = pd.read_csv(args.classification_result_fn,sep="\t",dtype={"authorZipCode":str})
df_data = pd.read_csv(args.data_fn,dtype={"authorZipCode":str})

data = {}
for lex in lexiques:
    if not lex in data:
        data[lex]={}
    for q in df_classification.columns[:-4]:
        print("Processing Lexique {0} and question {1}".format(lex,q))
        data_question  = get_question_with_transport_data(df_data,df_classification,q)
        if not args.s:
            lemmas = lemmatize(data_question,fr_stop,lemmatizer="talismane")
        else:
            lemmas = lemmatize(data_question,fr_stop,lemmatizer="spacy")
        matched_words = match_lexique_to_responses_texts(lemmas,lexiques[lex])
        count_dict = count_occurrences(matched_words,lexique_dataframe=lexiques[lex],binary=True,min_support=10)
        data[lex][q]=count_dict

output_fn_suffix = args.data_fn.split("/")[-1]
json.dump(data,open("terms_count_{0}.json".format(output_fn_suffix),'w'))