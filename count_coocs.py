import argparse

import numpy as np
import pandas as pd
from tqdm import tqdm

# Custom library
from lib.textometry import *
from lib.helpers import *
from lib.constant import *
from lib.cooc import *


from lib.utils import partofspeech
from stop_words import get_stop_words
fr_stop = get_stop_words("french")


# Pandas shoots warning non-stop ... so chouh !
import warnings
warnings.simplefilter(action='ignore', category=pd.errors.DtypeWarning)

code_questions = {
    1:"transition_eco",
    2:"democratie_et_citoy",
    3:"fiscalite_et_depense_publique",
    4:"organisation_de_etat_et_service_pub"
}

parser = argparse.ArgumentParser()
parser.add_argument("data_fn")
parser.add_argument("classification_result_fn")
parser.add_argument("dataset_code",help=";".join(["{0} - {1} ".format(k,v)for k,v in code_questions.items()]))
parser.add_argument("-s",action="store_true",help="Use Spacy to lemmatize")



args = parser.parse_args()#("data/LA_TRANSITION_ECOLOGIQUE.csv data/transition_eco.csv -s".split())


##### LOAD ANNOTATION AND ORIGINAL DATASET
df_data = pd.read_csv(args.data_fn,dtype={"authorZipCode":str})
df_classification = pd.read_csv(args.classification_result_fn,sep="\t",dtype={"authorZipCode":str})


######### IDENTIFICATION OF PATTERNS
treatments = [ChangementAttributTransport(),ChangementTransport(),ShortPhrases()]
final_data = []
for question in tqdm(analysed_questions[code_questions[args.dataset_code]]):
    data_question  = get_question_with_transport_data(df_data,df_classification,question).values
    if not args.s:
        data_reponse = partofspeech(data_question,fr_stop,lemmatizer="talismane")
    else:
        data_reponse = partofspeech(data_question,fr_stop,lemmatizer="spacy")
    matching_datas = get_matching_data([np.asarray(d)[:,2] for d in data_reponse])
    zipcodes = df_data[df_classification[question].values.astype(bool)]["authorZipCode"].values
    references = df_data[df_classification[question].values.astype(bool)]["reference"].values
    for i in range(len(references)):
        for p in treatments:
            c = Contribution(np.array(data_reponse[i]),matching_datas[i],column=2)
            res = c.apply(p,question.split(" - ")[0],references[i],zipcodes[i])
            final_data.extend(res)

output_fn_suffix = args.data_fn.split("/")[-1]
df_cooc = pd.DataFrame(final_data,columns=["Part1","Part2","Part3","RelationType","Text","Question","Reference","authorZipCode"])
df_cooc.to_csv("cooc_data_{0}.csv".format(output_fn_suffix),sep="\t",index=False)