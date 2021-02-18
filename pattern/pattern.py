# coding = utf-8

class Pattern():
    """"""

    def __init__(self,name):
        """Constructor for Pattern"""
        self.__name = name
        self.index_to_field = {}

    def get_patterns(self):
        raise NotImplemented()

    def parse_output(self,matches):
        results_dict = {}
        for m in matches:
            pass
        return results_dict

    @property
    def name(self):
        return self.__name


