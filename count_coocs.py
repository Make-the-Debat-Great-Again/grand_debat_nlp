import argparse

import numpy as np
import pandas as pd
from tqdm import tqdm

# Custom library
from lib.textometry import *
from lib.helpers import *
from lib.constant import *
from lib.cooc import *

# Pandas shoots warning non-stop ... so chouh !
import warnings
warnings.simplefilter(action='ignore', category=pd.errors.DtypeWarning)

parser = argparse.ArgumentParser()
parser.add_argument("data_fn")
parser.add_argument("classification_result_fn")

args = parser.parse_args()


##### LOAD ANNOTATION AND ORIGINAL DATASET
df_data = pd.read_csv(args.data_fn,dtype={"authorZipCode":str})
df_classification = pd.read_csv(args.classification_result_fn,sep="\t",dtype={"authorZipCode":str})


######### IDENTIFICATION OF PATTERNS
treatments = [ChangementAttributTransport(),ChangementTransport(),ShortPhrases()]
final_data = []
for question in tqdm(analysed_questions['transition_eco']):
    data_question  = get_question_with_transport_data(df_data,df_classification,question).values
    data_reponse = get_data_from_texts(data_question)
    matching_datas = get_matching_data([d[:,2] for d in data_reponse])
    zipcodes = df_data[df_classification[question].values.astype(bool)]["authorZipCode"].values
    references = df_data[df_classification[question].values.astype(bool)]["reference"].values
    for i in range(len(references)):
        for p in treatments:
            c = Contribution(data_reponse[i],matching_datas[i],column=2)
            res = c.apply(p,question.split(" - ")[0],references[i],zipcodes[i])
            final_data.extend(res)

df_cooc = pd.DataFrame(final_data,columns=["Part1","Part2","Part3","RelationType","Question","Reference","authorZipCode"])
df_cooc.to_csv("cooc_data.csv",sep="\t",index=False)