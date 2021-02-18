# coding = utf-8

from .pattern import Pattern

class ObservationObjectif(Pattern):
    """"""

    def __init__(self):
        """Constructor for ObservationObjectif"""
        super(ObservationObjectif, self).__init__(self.__name__())

    def get_patterns(self):
        cod = [
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

        cod_neg = [
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
                "RIGHT_ATTRS": {"POS": {"IN": ["NOUN", "VERB"]}, "DEP": "obj"}
            },
            {
                "LEFT_ID": "verbe",
                "REL_OP": ">",
                "RIGHT_ID": "neg",
                "RIGHT_ATTRS": {"DEP": "advmod", "ORTH": {"IN": ["n'", "ne", "pas", "plus"]}}
            }
        ]
        return [cod,cod_neg]