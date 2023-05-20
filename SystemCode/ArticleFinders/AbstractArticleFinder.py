"""The abstract base ArticleFinder class which all Finder must subclass."""

from abc import ABC, abstractmethod
from datetime import datetime

class AbstractArticleFinder(ABC):
    @abstractmethod
    def find(self, from_date: datetime, to_date: datetime)-> list:
        """
        All Handlers must override the `find` method,
        which must return a DataFrame.
        """

class ArticleFinderError(Exception):
    """An Error exception raised during the operation of a ArticleFinder"""