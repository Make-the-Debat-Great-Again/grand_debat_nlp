# coding = utf-8

from .pattern import Pattern
import copy

class ObservationObjectif(Pattern):
    """"""

    def __init__(self):
        """Constructor for ObservationObjectif"""
        Pattern.__init__(self,"ObservationObjectif")

    def get_patterns(self):
        patterns =  {"sujetverbecod":[
            {
                "RIGHT_ID": "sujet",
                "RIGHT_ATTRS": {"POS": "NOUN", "DEP": {"IN": ["nsubj", "nsubj:pass"]}}
            },
            {
                "LEFT_ID": "sujet",
                "REL_OP": "<",
                "RIGHT_ID": "verbe",
                "RIGHT_ATTRS": {}
            },
            {
                "LEFT_ID": "verbe",
                "REL_OP": ">",
                "RIGHT_ID": "cod",
                "RIGHT_ATTRS": {"POS": "NOUN", "DEP": "obj"}
            }
            ]
        }
        patterns["cod_neg"] = self.get_neg(patterns["sujetverbecod"],"verbe")
        return patterns

    def is_valid(self,doc,match):
        return True


class Proposition(Pattern):
    """"""

    def __init__(self):
        """Constructor for Proposition"""
        Pattern.__init__(self,"PROPOSITION")
        self.index_to_field = {}


    def get_patterns(self):
        proposition = {
            "pat_actor_do_action_on_target": [ # Les entreprises doivent payer leur impot
                {
                    "RIGHT_ID": "objet",
                    "RIGHT_ATTRS": {"POS": "NOUN", "DEP": {"IN": ["obj"]}}
                },
                {
                    "LEFT_ID": "objet",
                    "REL_OP": "<",
                    "RIGHT_ID": "verbe",
                    "RIGHT_ATTRS": {"POS": "VERB", "DEP": "xcomp"}
                },
                {
                    "LEFT_ID": "verbe",
                    "REL_OP": "<",
                    "RIGHT_ID": "verbe2",
                    "RIGHT_ATTRS": {"POS": "VERB", "DEP": "ROOT"}
                },
                {
                    "LEFT_ID": "verbe2",
                    "REL_OP": ">",
                    "RIGHT_ID": "acteur",
                    "RIGHT_ATTRS": {"POS": "NOUN", "DEP": "nsubj"}
                }
            ],
            "pat_sujet_verb":[ # Augmenter les impots
            {
                "RIGHT_ID": "objet",
                "RIGHT_ATTRS": {"POS": "NOUN", "DEP": {"IN": ["obj"]}}
            },
            {
                "LEFT_ID": "objet",
                "REL_OP": "<",
                "RIGHT_ID": "verbe",
                "RIGHT_ATTRS": {"POS": "VERB", "DEP": "ROOT"}
            }],

            "pat_adv_sujet": [ # Plus d'impots
                {
                    "RIGHT_ID": "objet",
                    "RIGHT_ATTRS": {"POS": "NOUN"}
                },
                {
                    "LEFT_ID": "objet",
                    "REL_OP": ">",
                    "RIGHT_ID": "adverbe",
                    "RIGHT_ATTRS": {"POS": "ADV", "LEMMA": {"IN": ["plus","moins"]}}
                }]
        }
        left_id={"pat_sujet_verb":"verbe","pat_adv_sujet":"adverbe","pat_acteur_verbx2_obj":"verbe2","pat_actor_do_action_on_target":"verbe2"}
        for pat_key,pat_val in copy.copy(proposition).items():
            proposition[pat_key+"_neg"] = self.get_neg(pat_val, left_id[pat_key])
        return proposition



    def is_valid(self,doc,match):
        for i in match[-1]:
            # Pas de pronom personnel --> ex. J'utilise ma voiture.
            if doc[i].pos_ == "VERB":
                if doc[i].lemma_ == "avoir":
                    return False
                for child in doc[i].children:
                    if child.pos_ == "PRON":
                        return False
        return True

