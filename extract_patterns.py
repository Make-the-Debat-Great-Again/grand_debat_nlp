# coding = utf-8
import spacy
from spacy import displacy

import pandas as pd
from tqdm import tqdm
from lib.constant import analysed_questions,question_patterns

from spacy.matcher import DependencyMatcher
from pattern import enjeux
import json
import os
import argparse

index_pattern = {
    1: "OBSERVATION",
    2: "PROPOSITION",
    3: "ITEMLIST",
    4: "SITUATIONPERSONNELLE"
}

parser = argparse.ArgumentParser()
parser.add_argument("dataset_code",choices=list(question_patterns.keys()))
parser.add_argument("dataset_fn")
parser.add_argument("-n","--n-process",default=1,type=int)

args= parser.parse_args()

output_dir = os.path.join("./","output_{0}".format(args.dataset_code))
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# INIT SPACY MODEL
nlp = spacy.load("fr_core_news_lg")
nlp.add_pipe("merge_noun_chunks")

# DATA
df_data = pd.read_csv(args.dataset_fn, dtype={"authorZipCode": str}).fillna("")

# PREPARE MATCHER
matcher = DependencyMatcher(nlp.vocab)
prop = enjeux.Proposition()
observ = enjeux.ObservationObjectif()

for pat_key, pat_value in observ.get_patterns().items():
    matcher.add("OBSERVATION|{0}".format(pat_key), [pat_value])
for pat_key, pat_value in prop.get_patterns().items():
    matcher.add("PROPOSITION|{0}".format(pat_key), [pat_value])

for question, pattern_idx in question_patterns[args.dataset_code].items():
    results = []
    id_ = df_data["id"].values
    zipCode = df_data["authorZipCode"].values
    data_question = df_data[question].values
    for ix, doc in tqdm(enumerate(nlp.pipe(data_question,n_process=args.n_process)), total=len(data_question)):
        question_res = []
        #response = nlp(doc)
        response = doc
        matches = matcher(response)
        if len(matches) > 0:
            for pat in pattern_idx:
                found = []
                if pat == 2:
                    found.extend(prop.parse_output(response,
                                                   [ma for ma in matches if
                                                    nlp.vocab.strings[ma[0]].split("|")[0] == "PROPOSITION"]))
                elif pat == 1:
                    found.extend(observ.parse_output(response,
                                                     [ma for ma in matches if
                                                      nlp.vocab.strings[ma[0]].split("|")[0] == "OBSERVATION"]))
                question_res.append(found)
            results.append([id_[ix], zipCode[ix], question_res,data_question[ix]])
    json.dump(results, open(output_dir+"/"+question.split(" - ")[0] + ".json", 'w'))
