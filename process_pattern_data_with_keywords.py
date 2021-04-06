# coding = utf-8
import numpy as np
import pandas as pd
import re
import editdistance
import json
import argparse
import ast
from french_lefff_lemmatizer.french_lefff_lemmatizer import FrenchLefffLemmatizer

parser =argparse.ArgumentParser()
parser.add_argument("input_fn")
parser.add_argument("output_fn")

args = parser.parse_args()

input_fn = args.input_fn
output_fn = args.output_fn

df = pd.read_csv(input_fn, sep="\t", index_col=0,
                 dtype={"code_postal": str}, converters={c: ast.literal_eval for c in
                                                         ['keywords_in_text', 'keywords_in_onto', 'class_lvl_4',
                                                          'class_lvl_3', 'class_lvl_2', 'class_lvl_1']}).fillna("")

lemmatizer = FrenchLefffLemmatizer()

df["verbe"] = df.verbe.apply(lambda x : re.sub("[^A-Za-zéèëâàäiîïoôöùûü]+","",x) )
df["verbe"] = df.verbe.apply(lemmatizer.lemmatize,args=('v')).apply(str.lower)

df["verbe2"] = df.verbe2.apply(lambda x : re.sub("[^A-Za-zéèëâàäiîïoôöùûü]+","",x) )
df["verbe2"] = df.verbe2.apply(lemmatizer.lemmatize,args=('v')).apply(str.lower)

all_fr_verbs = list(json.load(open("resources/lexiques/verbs-fr.json")).keys())


def correct_verb(verb_x):
    if verb_x in all_fr_verbs:
        return verb_x
    else:
        min_dist = 9999999
        closest_verb =verb_x
        for verb in all_fr_verbs:
            dist_=editdistance.eval(verb_x,verb)
            if dist_ < min_dist:
                closest_verb = verb
                min_dist = dist_
            if dist_ <2:
                break
        if min_dist>2:
            return verb_x
        return closest_verb

verbs = np.unique(np.concatenate((df.verbe.unique(),df.verbe2.unique())))
correction_dict= {verb:correct_verb(verb) for verb in verbs}

df["verbe"] = df.verbe.apply(lambda x: correction_dict[x])
df["verbe2"] = df.verbe2.apply(lambda x: correction_dict[x])

def verb_is_valid(verb,allow_empty=False):
    if len(verb) == 0 and allow_empty:
        return True
    if verb in ("être","avoir","plus","moins"):
        return True
    for end in "er ir oir re".split():
        if verb.endswith(end):
            return True
    return False
df = df[df.verbe.apply(verb_is_valid)]
df = df[df.verbe2.apply(lambda x :verb_is_valid(x,allow_empty=True))]
df = df.drop_duplicates("id_contrib question_id verbe2 acteur verbe objet".split(),keep="last")

for col in ['keywords_in_text','keywords_in_onto', 'class_lvl_4', 'class_lvl_3', 'class_lvl_2','class_lvl_1']:
    df[col]= df[col].apply(lambda x : "|".join(x))

df["neg"] = df.neg.apply(lambda x : 1 if x else 0)

df.to_csv(output_fn,sep="\t")