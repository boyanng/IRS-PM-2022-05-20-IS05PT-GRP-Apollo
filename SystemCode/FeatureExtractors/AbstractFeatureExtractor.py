"""The abstract base FeatureExtractor class which all Extractor must subclass."""

from abc import ABC, abstractmethod
import spacy

class AbstractFeatureExtractor(ABC):
    """All Feature must inherit from this AbstractFeatureExtractor class."""

    def __init__(self, nlp_model=None):
        """
        All Handlers must input NLP Model to be used, defaul will be using spacy en_core_web_sm
        """
        if nlp_model == None:
            self.nlp = spacy.load("en_core_web_sm")
        else:
            self.nlp = nlp_model

    @abstractmethod
    def extract(self, text):
        """
        All Handlers must override the `extract` method,
        which must return a list of string.
        """


class ExtractorError(Exception):
    """An Error exception raised during the operation of a Extractor."""
