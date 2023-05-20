import spacy
from FeatureExtractors.AbstractFeatureExtractor import AbstractFeatureExtractor

class KeywordExtractor(AbstractFeatureExtractor):
    """A class to extract whether there is any keywords
    
    Arguments:
        keywords: keywords to be used
        nlp_model: NLP model to be used
    """
    def __init__(self,keywords: list, nlp_model=None):
        super().__init__(nlp_model)
        self.keywords = keywords
        
    def extract(self,text: str):
        """Extract Information

        Arguments:
        text: text to extract information from
        
        """
        doc = self.nlp(text)
        
        preprocessed_sentence=[]
        for token in doc:
            if token.pos_ != 'PUNCT' and token.is_stop is False:
                preprocessed_sentence.append(token)
        result = []
        for token in preprocessed_sentence:
            if token.lemma_.lower() in self.keywords:
                    result+= [token.lemma_.lower()]
        return list(set(result))


    
