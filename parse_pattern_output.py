# coding = utf-8
import json
import pandas as pd
import glob
import numpy as np
from tqdm import tqdm
tqdm.pandas()
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("input_dir")

args = parser.parse_args()
dir_ = args.input_dir


dfs_prop = []
dfs_obs = []
dfs_s_p=[]

dataset_name = dir_.split("/")[-1][len("output_"):]
fns = glob.glob(dir_+"/*.json")

for fn in fns:
    question_id = fn.split("/")[-1].strip(".json")
    data = json.load(open(fn))
    motifs_obs = []
    motifs_prop = []
    motifs_sit_per = []
    for item in data:
        id_ = item[0]
        cp_ = item[1]
        #doc = item[-1]
        for x in item[-2]:
            for i in x:
                i.update({"id_contrib":id_,"code_postal":cp_})#,"doc":doc})
                if i["type"] == "ObservationObjectif":
                    motifs_obs.append(i)
                elif i["type"] == "Proposition":
                    motifs_prop.append(i)
                else:
                    motifs_sit_per.append(i)

    df_obs = pd.DataFrame(motifs_obs)
    df_obs["question_id"] = question_id
    df_props = pd.DataFrame(motifs_prop)
    df_props["question_id"] = question_id
    df_s_p = pd.DataFrame(motifs_sit_per)
    df_s_p["question_id"] = question_id

    if len(df_obs) > 0:
        df_obs = df_obs["id_contrib question_id code_postal neg sujet verbe cod type pattern_name".split()]
        dfs_obs.append(df_obs)

    if len(df_props) > 0:
        df_props= df_props["id_contrib question_id code_postal neg adverbe verbe2 acteur verbe objet type pattern_name".split()]
        dfs_prop.append(df_props)

    if len(df_s_p) > 0:
        df_s_p = df_s_p["id_contrib question_id code_postal neg pers_pronoun verb subject type pattern_name".split()]
        dfs_s_p.append(df_s_p)

pd.concat(dfs_obs).to_csv("{0}.csv".format(dataset_name+"_obs"),sep="\t")
pd.concat(dfs_prop).to_csv("{0}.csv".format(dataset_name+"_prop"),sep="\t")
if len(dfs_s_p)>0:pd.concat(dfs_s_p).to_csv("{0}.csv".format(dataset_name+"_sit_per"),sep="\t")