import spacy
from FeatureExtractors.AbstractFeatureExtractor import AbstractFeatureExtractor

class DiseaseExtractor(AbstractFeatureExtractor):
    """A class to extract diseases
    
    Arguments:
        nlp_model: NLP model to be used
    """
    def extract(self, text: str):
        """Extract Information

        Arguments:
        text: text to extract information from
        
        """
        doc = self.nlp(text)
        diseases = []
        for ent in doc.ents:
            if ent.label_ == "DISEASE":
                    diseases+= [ent.text.upper()]
        return diseases
    
