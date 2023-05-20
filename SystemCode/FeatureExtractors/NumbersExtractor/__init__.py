import spacy
from FeatureExtractors.AbstractFeatureExtractor import AbstractFeatureExtractor
import numpy as np
from numerizer import numerize
import number_parser

def string2num(txt):
        if txt.ent_type_=='ORDINAL':
            return float(number_parser.parse_ordinal(txt.text))
        elif txt.like_num :
            if "," in txt.text:
                return float(numerize(txt.text.replace(',','')))
            else:
                return float(number_parser.parse_ordinal(txt.text))
        else:
            raise ValueError('Handler cant convert this to number')

class NumberExtractor(AbstractFeatureExtractor):
    """A class to extract number
        keyword: keyword of the number to be used
    """
    def __init__(self,keywords: list, nlp_model=None):
        super().__init__(nlp_model)
        self.keywords = keywords
        

    def extract(self, text: str):
        """Extract Information
        
        Arguments:
            nlp_model: NLP model to be used
        """
        doc = self.nlp(text)
        numbers = np.nan
        for token in doc:
            if token.lemma_.lower() in self.keywords:
                numbers =  self.extract_number_with_keywords(token)
                if np.isnan(numbers):
                    numbers =  self.extract_number_with_nsub_of_keyword(token)

        return numbers
    
    def extract_number_with_keywords(self, token: spacy.tokens.token.Token):
        extracted_list = []
        number = [c for c in token.children if c.like_num]
        extracted_list = number
        for n in extracted_list:
            if n.like_num or n.ent_type_=='ORDINAL' or n.ent_type_=='CARDINAL' or n.pos_ =='NUM': # check numbers next to keyword
                extracted_list+=[c for c in n.children if c.like_num]
        extracted_list = [string2num(e) for e in extracted_list]
        if len(extracted_list)>0:
            return sum(extracted_list)
        else:
            return np.nan
    
    def extract_number_with_nsub_of_keyword(self, token: spacy.tokens.token.Token):
            extracted_list = []
            nsubs = [a for a in token.children if a.dep_ == 'nsubj' and a.pos_ == 'NOUN']
            for sub in nsubs:
                extracted_list+=[c for c in sub.children if c.like_num]
            extracted_list = [string2num(e) for e in extracted_list]
            if len(extracted_list)>0:
                return sum(extracted_list)
            else:
                return np.nan
