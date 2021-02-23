# coding = utf-8
import spacy
from spacy import displacy

import pandas as pd
from tqdm import tqdm
from lib.constant import analysed_questions

from spacy.matcher import DependencyMatcher
from pattern import enjeux
import json

index_pattern = {
    1:"OBSERVATION",
    2:"PROPOSITION"
}

question_patterns = {
    'QUXVlc3Rpb246MTYx - Que faudrait-il faire selon vous pour apporter des réponses à ce problème ?': [2],
    'QUXVlc3Rpb246MTQ3 - Si oui, de quelle manière votre vie quotidienne est-elle touchée par le changement climatique ?': [1],
    "QUXVlc3Rpb246MTUw - Qu'est-ce qui pourrait vous inciter à changer vos comportements comme par exemple mieux entretenir " \
    + "et régler votre chauffage, modifier votre manière de conduire ou renoncer à prendre votre véhicule pour de très petites distances ?": [2],
    'QUXVlc3Rpb246MTUx - Quelles seraient pour vous les solutions les plus simples et les plus supportables sur un plan financier pour vous inciter à changer vos comportements ?': [2],
    'QUXVlc3Rpb246MTU1 - Si oui, que faudrait-il faire pour vous convaincre ou vous aider à utiliser ces solutions alternatives ?': [2],
    "QUXVlc3Rpb246MjA3 - Si non, quelles sont les solutions de mobilité alternatives que vous souhaiteriez pouvoir utiliser ?": [2]
    }

# INIT SPACY MODEL
nlp = spacy.load("fr_core_news_lg")
nlp.add_pipe("merge_noun_chunks")

# DATA
df_data = pd.read_csv("data/LA_TRANSITION_ECOLOGIQUE.csv", dtype={"authorZipCode": str}).fillna("")


# PREPARE MATCHER
matcher = DependencyMatcher(nlp.vocab)
prop = enjeux.Proposition()
observ = enjeux.ObservationObjectif()

for pat_key,pat_value in observ.get_patterns().items():
    matcher.add("OBSERVATION|{0}".format(pat_key), [pat_value])
for pat_key,pat_value in prop.get_patterns().items():
    matcher.add("PROPOSITION|{0}".format(pat_key), [pat_value])

for question,pattern_idx in question_patterns.items():
    results = []
    id_ = df_data["id"].values
    zipCode = df_data["authorZipCode"].values
    data_question = df_data[question].values
    for ix, doc in tqdm(enumerate(data_question),total=len(data_question)):
        question_res = []
        response = nlp(doc)
        matches = matcher(response)
        if len(matches)>0:
            for pat in pattern_idx:
                found = []
                if pat == 2:
                    found.extend(prop.parse_output(response,
                                  [ma for ma in matches if nlp.vocab.strings[ma[0]].split("|")[0] == "PROPOSITION"]))
                else:
                    found.extend(observ.parse_output(response,
                                    [ma for ma in matches if nlp.vocab.strings[ma[0]].split("|")[0] == "OBSERVATION"]))
                question_res.append(found)
            results.append([id_[ix],zipCode[ix],question_res])
    json.dump(results,open(question.split(" - ")[0]+".json",'w'))



