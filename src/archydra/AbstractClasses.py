from abc import ABC,abstractmethod
from typing import Iterable

class Producer(ABC):
    @abstractmethod
    def get_urls(self) -> Iterable[str]:
        """
        Get the URLs from the producer
        
        :return: An Iterable of strings
        :rtype: Iterable[str]
        """
        pass

class Consumer(ABC):
    @abstractmethod
    def process_url(self, url:str) -> None:
        """
        Process a URL
        
        :param url: Description
        :type url: str
        """
        pass