# coding = utf-8
import copy


class Pattern():
    """"""

    def __init__(self,name):
        """Constructor for Pattern"""
        self.__name = name
        self.index_to_field = {}

    def get_patterns(self):
        raise NotImplemented()

    def parse_output(self, doc, matches):
        results = []
        patterns = self.get_patterns()
        for match in matches:
            if self.is_valid(doc, match):
                key_match = doc.vocab.strings[match[0]].split("|")[-1]

                res = {}
                for ix, id_ in enumerate(match[1]):
                    res[patterns[key_match][ix]["RIGHT_ID"]] = doc[id_].text
                res["type"] = self.__class__.__name__
                res["pattern_name"]=key_match
                results.append(res)
        return results

    @property
    def name(self):
        return self.__name

    def get_neg(self,pattern, left_id):
        new_pattern = copy.copy(pattern)
        new_pattern.append(
            {
                "LEFT_ID": left_id,
                "REL_OP": ">",
                "RIGHT_ID": "neg",
                "RIGHT_ATTRS": {"DEP": "advmod", "ORTH": {"IN": ["n'", "ne", "pas"]}}
            })
        return new_pattern

    def is_valid(self,doc,match):
        raise NotImplemented()

