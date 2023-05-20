import spacy
from FeatureExtractors.AbstractFeatureExtractor import AbstractFeatureExtractor

class OrganisationExtractor(AbstractFeatureExtractor):
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
            if ent.label_ == "ORG":
                    locations+= [ent.text.upper()]
        return locations
    
