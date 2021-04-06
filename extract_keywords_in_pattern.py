# coding = utf-8

import pandas as pd
from tqdm import tqdm
import spacy
from owlready2 import get_ontology
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("input_fn")
args = parser.parse_args()

input_fn = args.input_fn #"outputs/parsed_v4/transition_eco_prop.csv"


def get_ordered_ancestors(class_,include_self=False):
    c = class_
    res= []
    if include_self:
        res.append(c)
    while 1:
        c = c.is_a
        if len(c)<1:
            break
        c = c[0]
        res.append(c)
    return res

# LOAD ONTOLOGY
onto = get_ontology("resources/lexiques/transportonto4.owl")
onto.load()
classes = list(onto.classes())
ontology_data = []
for c in classes[1:]:
    try:
        ontology_data.append([str(c.name),str(c.prefLabel[0]),[str(lab)for lab in c.altLabel] ,c.iri])
    except:
        pass
df_ontologie = pd.DataFrame(ontology_data,columns="name prefLabel altLabel iri".split())

# LOAD DATA
df = pd.read_csv(input_fn,sep="\t",index_col=0,dtype={"code_postal":str}).fillna("")

# LOAD SPACY MODEL
nlp = spacy.load("fr_core_news_sm")
nlp.remove_pipe("ner")
ruler = nlp.add_pipe("entity_ruler")

# ADD PATTERN TO DETECT KEYWORDS
patterns = []
for ix,row in df_ontologie.iterrows():
    pattern_ = [{"LOWER":str(x.lower())} for x in row.prefLabel.split()]
    patterns.append({"label":row["name"],"pattern":pattern_})
    for alias in row.altLabel:
        pattern_ = [{"LOWER":x.lower()} for x in alias.split()]
        patterns.append({"label":row["name"],"pattern":pattern_})

for ix,row in df_ontologie.iterrows():
    pattern_ = [{"LEMMA":x.lower()} for x in row.prefLabel.split()]
    patterns.append({"label":row["name"],"pattern":pattern_})
    for alias in row.altLabel:
        pattern_ = [{"LEMMA":x.lower()} for x in alias.split()]
        patterns.append({"label":row["name"],"pattern":pattern_})
ruler.add_patterns(patterns)


def is_in_spacy(x):
    texts_, labels_ = [], []
    for ent in x.ents:
        texts_.append(ent.text)
        labels_.append(ent.label_)
    return texts_, labels_

#EXTRACT KEYWORDS
keywords_in_text, keywords_in_onto = [], []
for text in tqdm(nlp.pipe(df.objet.values, n_process=4), total=len(df)):
    texts, labels = is_in_spacy(text)
    keywords_in_text.append(texts)
    keywords_in_onto.append(labels)

df["keywords_in_text"], df["keywords_in_onto"] = keywords_in_text, keywords_in_onto


def get_nminus_k(c, k=1):
    l = k + 1
    ancestors = get_ordered_ancestors(c, include_self=True)
    if len(ancestors) == 0:
        return c
    if len(ancestors) < l:
        return get_nminus_k(c, k - 1)
    return ancestors[-l]

#STORE KEYWORDS UPPER CLASSES
name_class = {row["name"]: onto.search(prefLabel=row.prefLabel)[0] for ix, row in df_ontologie.iterrows()}
df["class_lvl_4"] = df.keywords_in_onto.apply(lambda key: [get_nminus_k(name_class[x], 1).name for x in key])
df["class_lvl_3"] = df.keywords_in_onto.apply(lambda key: [get_nminus_k(name_class[x], 2).name for x in key])
df["class_lvl_2"] = df.keywords_in_onto.apply(lambda key: [get_nminus_k(name_class[x], 3).name for x in key])
df["class_lvl_1"] = df.keywords_in_onto.apply(lambda key: [get_nminus_k(name_class[x], 4).name for x in key])

#SAVE
df.to_csv(input_fn.rstrip(".csv")+"_withkeywords_and_classes.csv",sep="\t")