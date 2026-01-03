from abc import ABC, abstractmethod
from typing import Iterable
from loguru import logger
from archydra.Helpers import roundrobin


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
    def process_url(self, url: str) -> None:
        """
        Process a URL

        :param url: Description
        :type url: str
        """
        pass


class Filter(Producer):
    """
    Special kind of producer that takes in other producers as input
    """

    def _roundrobin(self):
        logger.debug("Starting roundrobin")
        my_iterables = tuple(p.get_urls() for p in self.producers)
        yield from roundrobin(*my_iterables)

    def __init__(self, producers: list[Producer]) -> None:
        self.producers = producers
        super().__init__()
