import numpy as np
from .utils import parallel_talismane
from .textometry import match_lexique_to_responses_texts
from .constant import *

WINDOW_SIZE = 4
import re

def get_data_from_texts(texts,batch_size=1000,lemmas_only=False):
    def transform_and_return(df):
        df.LEMMA = df.apply(lambda x : x.FORM.lower() if x.LEMMA=="_" else x.LEMMA,axis=1)
        return df
    if lemmas_only:
        res = [transform_and_return(talismane_data).LEMMA.values for talismane_data in parallel_talismane(data=texts,batch_size=batch_size)]
    else:
        res = [transform_and_return(talismane_data).values for talismane_data in parallel_talismane(data=texts,batch_size=batch_size)]
    return res

def get_matching_data(lemmas):
    def get_dict(match_res,lexiques):
        dict_ = {}
        for m in match_res:
            dict_[m[1]] = m[0]
        return dict_
    transp_terms_matched = match_lexique_to_responses_texts(lemmas,lexiques["transport_term"],return_pos=True)
    change_verbs_matched = match_lexique_to_responses_texts(lemmas,lexiques["change_verb"],return_pos=True)
    attribut_matched = match_lexique_to_responses_texts(lemmas,lexiques["attribut"],return_pos=True)

    final_res = []
    for i in range(len(transp_terms_matched)):
        transp_=get_dict(transp_terms_matched[i],lexiques["transport_term"])
        attr_=get_dict(attribut_matched[i],lexiques["attribut"])
        chang_=get_dict(change_verbs_matched[i],lexiques["change_verb"])
        final_res.append({
                "transport_term": transp_,
                "change_verb":chang_,
                "attribut":attr_
        })
    return final_res


class Contribution(object):
    def __init__(self,text_data,matching_data_dict,column=None,phrase_separator=[".","?","!"],erase_temp_data=True):
        self.__text = text_data
        self.matching_data_dict = matching_data_dict
        self.column = column
        self.phrase_separator = phrase_separator    

        self.erase_temp_data = erase_temp_data

        self.split_in_sentences()
    
    def get_matched_for_a_sentence(self,begin_pos,end_pos):
        new_dict = {}
        for lexique in self.matching_data_dict:
            new_dict[lexique]={}
            for pos in self.matching_data_dict[lexique]:
                if pos <=end_pos and pos >= begin_pos:
                    new_dict[lexique][pos-begin_pos]=self.matching_data_dict[lexique][pos]
        return new_dict
        
    def split_in_sentences(self):
        self.sentences = []
        index_start = 0
        for i in range(len(self.__text)):
            if self.column and self.__text[i,self.column] in self.phrase_separator:
                matched_data = self.get_matched_for_a_sentence(index_start,i)
                s = Sentence(self.__text[index_start:i+1],matched_data)
                self.sentences.append(s)
                index_start=i+1
            elif not self.column and self.__text[i] in self.phrase_separator:
                matched_data = self.get_matched_for_a_sentence(index_start,i)
                s = Sentence(self.__text[index_start:i+1],matched_data)
                self.sentences.append(s)
                index_start=i+1
        
        if index_start == 0 and not self.sentences:
            self.sentences.append(Sentence(self.__text,self.matching_data_dict,True))

        if len(self.sentences) == 1:
            self.sentences[0].is_alone = True

        if self.erase_temp_data:
            del self.__text

    def apply(self,treatment,*args):
        results = []
        for sentence in self.sentences:
            sentence_results = treatment(sentence)
            for res in sentence_results:
                res.extend([*args])
            results.extend(sentence_results)
        return results

class Sentence():
    def __init__(self,data,matched_data,alone=False):
        self.data = data
        self.is_alone= alone
        self.lexique_matched = matched_data

class Treatement():
    def __init__(self,name):
        self.name = name
    
    def __call__(self,a):
        return self.parseSentence(a)

    def parseSentence(self,sentence):
        raise NotImplementedError()

class TransportAdjectif(Treatement):
    def __init__(self):
        Treatement.__init__(self,"TRAN + ADJ")
    
    def parseSentence(self,sentence):
        results = []

        pos_adj = np.argwhere(sentence.data[:,3] == "ADJ").flatten()
        N = len(pos_adj)
        for pos in sentence.lexique_matched["transport_term"]:
            term_index = sentence.lexique_matched["transport_term"][pos]
            term_str = lexiques["transport_term"].iloc[term_index].word
            A = np.array([pos]*N)
            diff =  pos_adj - A
            adj_selected = sentence.data[:,2][pos_adj[(diff>0) & (diff<WINDOW_SIZE)]]
            if len(adj_selected)>0:
                results.extend([[term_str,None,adj,self.name," ".join(sentence.data[:,1])] for adj in adj_selected if not re.match("\d+",adj) and adj not in term_str])
        return results

class AttributAdjectif(Treatement):
    def __init__(self):
        Treatement.__init__(self,"ATTR + ADJ")
    
    def parseSentence(self,sentence):
        results = []

        pos_adj = np.argwhere(sentence.data[:,3] == "ADJ").flatten()
        N = len(pos_adj)
        for pos in sentence.lexique_matched["attribut"]:
            term_index = sentence.lexique_matched["attribut"][pos]
            term_str = lexiques["attribut"].iloc[term_index].word
            A = np.array([pos]*N)
            diff = pos_adj - A 
            adj_selected = sentence.data[:,2][pos_adj[(diff>0) & (diff<WINDOW_SIZE)]]
            if len(adj_selected) >0:
                results.extend([["Q_SUBJ",term_str,adj,self.name," ".join(sentence.data[:,1])] for adj in adj_selected if not re.match("\d+",adj)])
        return results

class AttributTransport(Treatement):
    def __init__(self):
        Treatement.__init__(self,"ATTR + ADJ")


    def parseSentence(self,sentence):
        results = []

        for pos1 in sentence.lexique_matched["attribut"]:
            chang_word = lexiques["attribut"].iloc[sentence.lexique_matched["attribut"][pos1]].word
            for pos2 in sentence.lexique_matched["transport_term"]:
                transp_word = lexiques["transport_term"].iloc[sentence.lexique_matched["transport_term"][pos2]].word
                diff = pos2-pos1
                if diff >0 and diff < WINDOW_SIZE:
                    results.append([chang_word,None,transp_word,self.name," ".join(sentence.data[:,1])])

        return results


class ChangementAttributTransport(Treatement):
    def __init__(self):
        Treatement.__init__(self,"CHG + ATTR + TRAN")
    
    def parseSentence(self,sentence):
        results = []

        for pos1 in sentence.lexique_matched["change_verb"]:
            chang_word = lexiques["change_verb"].iloc[sentence.lexique_matched["change_verb"][pos1]].word
            for pos2 in sentence.lexique_matched["transport_term"]:
                transp_word = lexiques["transport_term"].iloc[sentence.lexique_matched["transport_term"][pos2]].word
                diff = pos2-pos1
                if diff >0 and diff < WINDOW_SIZE:
                    for pos3 in sentence.lexique_matched["attribut"]:
                        if pos3 > pos1 and pos3 < pos2:
                            attr_word = lexiques["attribut"].iloc[sentence.lexique_matched["attribut"][pos3]].word
                            results.append([chang_word,attr_word,transp_word,self.name," ".join(sentence.data[:,1])])

        return results

class ChangementTransport(Treatement):
    def __init__(self):
        Treatement.__init__(self,"CHG + TRAN")
    
    def parseSentence(self,sentence):
        results = []

        for pos1 in sentence.lexique_matched["change_verb"]:
            chang_word = lexiques["change_verb"].iloc[sentence.lexique_matched["change_verb"][pos1]].word
            for pos2 in sentence.lexique_matched["transport_term"]:
                transp_word = lexiques["transport_term"].iloc[sentence.lexique_matched["transport_term"][pos2]].word
                diff = pos2-pos1
                if diff >0 and diff < WINDOW_SIZE:
                    results.append([chang_word,None,transp_word,self.name," ".join(sentence.data[:,1])])

        return results


class ChangementTransportAdjectif(Treatement):
    def __init__(self):
        Treatement.__init__(self,"CHG + ATTR + ADJ")
    
    def parseSentence(self,sentence):
        results = []
        pos_adj = np.argwhere(sentence.data[:,3] == "ADJ").flatten()
        sentence.lexique_matched["adjectif"] = {}
        for pos in pos_adj:
            sentence.lexique_matched["adjectif"][pos]=pos#sentence.data[:,2][pos]

        for pos1 in sentence.lexique_matched["change_verb"]:
            chang_word = lexiques["change_verb"].iloc[sentence.lexique_matched["change_verb"][pos1]].word
            for pos2 in sentence.lexique_matched["adjectif"]:
                adj_word = sentence.data[:,2][pos2]
                if re.match("\d+",adj_word):
                    continue
                diff = pos2-pos1
                if diff >0 and diff < WINDOW_SIZE:
                    for pos3 in sentence.lexique_matched["transport_term"]:
                        if pos3 > pos1 and pos3 < pos2:
                            transp_word = lexiques["transport_term"].iloc[sentence.lexique_matched["transport_term"][pos3]].word
                            if not adj_word in transp_word:
                                results.append([chang_word,transp_word,adj_word,self.name," ".join(sentence.data[:,1])])

        return results

class GratuiteTransport(Treatement):
    def __init__(self):
        Treatement.__init__(self,"GRATUITE + TRAN")
    
    def parseSentence(self,sentence):
        results = []
        pos_grat = np.argwhere(sentence.data[:,2] == "gratuité").flatten()
        sentence.lexique_matched["gratuité"] = {}
        for pos in pos_grat:
            sentence.lexique_matched["gratuité"][pos]=pos#sentence.data[:,2][pos]

        for pos1 in sentence.lexique_matched["gratuité"]:
            grat_word = "gratuité"
            for pos2 in sentence.lexique_matched["transport_term"]:
                transp_word = lexiques["transport_term"].iloc[sentence.lexique_matched["transport_term"][pos2]].word
                diff = pos2-pos1
                if diff >0 and diff < WINDOW_SIZE:
                    results.append([grat_word,None,transp_word,self.name," ".join(sentence.data[:,1])])

        return results


class ShortPhrases(Treatement):
    def __init__(self):
        Treatement.__init__(self,"ADD TRAN")
    
    def parseSentence(self,sentence):
        results = []
        if not sentence.lexique_matched["attribut"] and not sentence.lexique_matched["change_verb"] and sentence.is_alone:
            for pos2 in sentence.lexique_matched["transport_term"]:
                transp_word = lexiques["transport_term"].iloc[sentence.lexique_matched["transport_term"][pos2]].word
                results.append(["ajouter",None,transp_word,self.name," ".join(sentence.data[:,1])])

        return results

def is_between(pos1,pos2,pos3):
    return (pos1 <pos2) and (pos2 < pos3)

class IsThereSomeone(Treatement):
    def __init__(self):
        Treatement.__init__(self,"ISTHERESOMEONE?")
    
    def parseSentence(self,sentence):
        results = []
        if sentence.lexique_matched["change_verb"] and sentence.lexique_matched["transport_term"]:
            for pos1 in sentence.lexique_matched["change_verb"]:
                change_word = lexiques["change_verb"].iloc[sentence.lexique_matched["change_verb"][pos1]].word
                for pos2 in sentence.lexique_matched["transport_term"]:
                    transp_word = lexiques["transport_term"].iloc[sentence.lexique_matched["transport_term"][pos2]].word
                    if pos2-pos1 < WINDOW_SIZE and pos2-pos1 >0:
                        if sentence.lexique_matched["attribut"]:
                              for pos3 in sentence.lexique_matched["attribut"]:
                                attr_word = lexiques["attribut"].iloc[sentence.lexique_matched["attribut"][pos3]].word
                                if is_between(pos1,pos3,pos2):
                                    results.append([change_word,attr_word,transp_word,pos1,pos3,pos2,self.name," ".join(sentence.data[:,1])])    
                        else:
                            results.append([change_word,None,transp_word,pos1,None,pos2,self.name," ".join(sentence.data[:,1])])

        if not sentence.lexique_matched["change_verb"] and not sentence.lexique_matched["transport_term"]:
            results.append([None,None,None,None,None,None,"CONTRE-EXEMPLE"," ".join(sentence.data[:,1])])

        return results
 