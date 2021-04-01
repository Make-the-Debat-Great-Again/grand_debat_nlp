# coding = utf-8
from .pattern import Pattern

class SituationPersonnelle(Pattern):
    """"""

    def __init__(self):
        """Constructor for ObservationObjectif"""
        Pattern.__init__(self,"SituationPersonnelle")

    def get_patterns(self):
        patterns =  {"pron_verb_noun":[
                  {
                    "RIGHT_ID": "subject",
                    "RIGHT_ATTRS": {
                      "POS": "NOUN","DEP":{"IN":["obl:agent","obj","obl:arg"]}
                    }
                  },
                  {
                    "LEFT_ID": "subject",
                    "REL_OP": "<",
                    "RIGHT_ID": "verb",
                    "RIGHT_ATTRS": {"POS":"VERB","MORPH":{"REGEX": ".*(?!Mood=Cnd).*((Tense=(Pres|Past))|(VerbForm=Inf))+.*"}
                    }
                  },
                  {
                    "LEFT_ID": "verb",
                    "REL_OP": ">",
                    "RIGHT_ID": "pers_pronoun",
                    "RIGHT_ATTRS": {
                      "DEP": {"IN":["nsubj","nsubj:pass"]},"LEMMA":{"IN":["je","nous"]}
                    }
                  }
                ],
            "acteurproche_verb_noun": [
                {
                    "RIGHT_ID": "subject",
                    "RIGHT_ATTRS": {
                        "POS": "NOUN", "DEP": {"IN": ["obl:agent", "obj", "obl:arg"]}
                    }
                },
                {
                    "LEFT_ID": "subject",
                    "REL_OP": "<",
                    "RIGHT_ID": "verb",
                    "RIGHT_ATTRS": {"POS": "VERB",
                                    "MORPH": {"REGEX": ".*(?!Mood=Cnd).*((Tense=(Pres|Past))|(VerbForm=Inf))+.*"}
                                    }
                },
                {
                    "LEFT_ID": "verb",
                    "REL_OP": ">",
                    "RIGHT_ID": "acteur_proche",
                    "RIGHT_ATTRS": {
                        "DEP": {"IN": ["nsubj", "nsubj:pass"]}, "LOWER": {"REGEX": "(mon |ma |mes |notre |nos )+.*"}
                    }
                }
            ]
        }
        patterns["cod_neg"] = self.get_neg(patterns["pron_verb_noun"],"verb")
        return patterns

    def is_valid(self,doc,match):
        return True