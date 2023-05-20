import spacy
from FeatureExtractors.AbstractFeatureExtractor import AbstractFeatureExtractor

class LocationExtractor(AbstractFeatureExtractor):
    """A class to extract location
    
    Arguments:
        nlp_model: NLP model to be used
    """
    def extract(self, text: str):
        """Extract Information

        Arguments:
        text: text to extract information from
        
        """
        doc = self.nlp(text)
        locations = []
        for ent in doc.ents:
            if ent.label_ == "LOC" or ent.label_ == "GPE":
                    locations+= [ent.text.upper()]
        return locations
    
