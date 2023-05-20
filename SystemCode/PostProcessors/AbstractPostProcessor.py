"""The abstract base PostProcessor class which all PostProcess Class must subclass."""

from abc import ABC, abstractmethod
from typing import Optional, Union

class AbstractPostProcessor(ABC):
    """All Feature must inherit from this AbstractPostProcessor class."""

    def process(self,input:Union[list,str]):
        """
        All Handlers must override the `process` method,
        which must return a list.
        """


class PostProcessorError(Exception):
    """An Error exception raised during the operation of a PostProcessor."""
