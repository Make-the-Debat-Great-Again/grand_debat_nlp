from flask import Flask,render_template,jsonify,request
import pandas as pd
import numpy as np
import sqlite3
import geopandas as gpd
import json
from editdistance import distance
from collections import OrderedDict
import re 

app = Flask(__name__)

# LOAD DATA
con = sqlite3.connect("./transition_eco_prop_withkeywords_and_classes_and_polarity.db",check_same_thread=False)
def regexp(pattern, input):
    return bool(re.match(pattern, input))
con.create_function('regexp', 2, regexp)

# LOAD VERBS
all_verbs = pd.read_sql_query("select distinct(verbe) from transition_eco",con)["verbe"].values.tolist()
all_verbs.extend(pd.read_sql_query("select distinct(verbe2) from transition_eco",con)["verbe2"].values.tolist())
all_verbs = list(set(all_verbs))

from owlready2 import get_ontology
onto = get_ontology("resources/lexiques/transportonto4.owl")
onto.load()
classes = list(onto.classes())
ontology_data = []
for c in classes[1:]:
    try:
        ontology_data.append([str(c.name),str(c.prefLabel[0]),[str(lab)for lab in c.altLabel] ,c.iri])
    except:
        pass

df_ontolgie = pd.DataFrame(ontology_data,columns="name prefLabel altLabel iri".split())

# LOAD OBJECT
all_objects = df_ontolgie.name.values

# FEATURES
def get_ordered_ancestors(class_,include_self=False):
    c = class_
    res= []
    if include_self:
        res.append(str(c.name))
    while 1:
        c = c.is_a
        if len(c)<1:
            break
        c = c[0]
        res.append(str(c.name))
    return res

all_features = []
for c in classes[1:]:
    ancestors = get_ordered_ancestors(c)
    if "caractéristique" in ancestors:
        all_features.append(c.name)


@app.route("/")
def home():
    return render_template("skeleton.html")


@app.route('/verbs',methods=["POST","GET"])
def get_verbs():
    term = request.get_json().get("q")
    results = ranked_dist(term,all_verbs)
    data = OrderedDict({})
    data["results"] = []
    i=0
    for res in results:
        data["results"].append({"id":res,"text":res})
        if i >5:break
        i+=1
    return jsonify(data)

@app.route('/objects',methods=["POST","GET"])
def get_objects():
    term = request.get_json().get("q")
    results = ranked_dist(term,all_objects)
    data = OrderedDict({})
    data["results"] = []
    i=0
    for res in results:
        data["results"].append({"id":res,"text":res})
        if i >5:break
        i+=1
    return jsonify(data)

@app.route("/features",methods=["POST","GET"])
def get_features():
    term = request.get_json().get("q")
    
    results = ranked_dist(term,all_features)
    data = OrderedDict({})
    data["results"] = []
    i = 0
    for res in results:
        data["results"].append({"id":res,"text":res})
        if i >5:break
        i+=1
    return jsonify(data)
    

@app.route("/get_geo_data")
def dep_data():  
    return jsonify(json.load(open("resources/geodata/departements_centroid.geojson")))

@app.route("/query" ,methods=['GET', 'POST'])
def query():
    content = request.get_json()
    selected_verb = content.get('verb', [])
    selected_feature =content.get('feat',[])
    selected_object = content.get('obj', [])
    selected_polarite = content.get('pol', None)
    if selected_polarite not in "-1 1 0".split():
        selected_polarite=None
    print(selected_verb,selected_object,selected_feature,selected_polarite)

    
    template="""
    select * from transition_eco
    where {0};
    """
    conditions = ""
    if selected_verb and not selected_polarite:
        conditions+="verbe REGEXP \".*({0}).*\"".format("|".join(selected_verb))

    if selected_feature:
        if selected_verb:
            conditions +=" and "
        conditions+="keywords_in_onto REGEXP \".*({0}).*\"".format("|".join(selected_feature))

    if selected_object:
        if selected_verb or selected_feature:
            conditions +=" and "
        conditions+="keywords_in_onto REGEXP \".*({0}).*\"".format("|".join(selected_object))

    if selected_polarite:
        if selected_verb or selected_feature or selected_object:
            conditions +=" and "
        conditions+="verbe_polarity == {0}".format(selected_polarite)

    print(template.format(conditions))
    selection = pd.read_sql_query(template.format(conditions),con)
    selection["dep_code"] = selection.code_postal.apply(lambda x : x[:2])
    counts = selection.groupby("dep_code",as_index=False).count()
    dep_count = dict(counts["dep_code verbe".split()].values)
    print(dep_count)
    return dep_count

def ranked_dist(word,other_words):
    df = pd.DataFrame(other_words,columns=["word"])
    df["dist"] = get_dist(word,other_words)
    df = df.sort_values(by="dist")
    return OrderedDict(dict(df.values))

def get_dist(word,other_words):
    return [distance(word,w) for w in other_words]

app.run(host="0.0.0.0",debug=True)

