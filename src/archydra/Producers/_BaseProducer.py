from abc import ABC, abstractmethod
from typing import Iterable

class BaseProducer(ABC):
    @abstractmethod
    def get_urls(self) -> Iterable[str]:
        """
        Get the URLs from the producer

        :return: An Iterable of strings
        :rtype: Iterable[str]
        """
        pass
