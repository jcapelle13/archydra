from abc import ABC,abstractmethod
from typing import Iterable
from itertools import cycle, islice
from loguru import logger

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

class Filter(Producer):
    """
    Special kind of producer that takes in other producers as input
    """
    def _roundrobin(self):
    # roundrobin('ABC', 'D', 'EF') → A D E B F C
    # Algorithm credited to George Sakkis
        logger.debug("Starting roundrobin")
        iterators = map(iter, [p.get_urls() for p in self.producers])
        for num_active in range(len(self.producers), 0, -1):
            iterators = cycle(islice(iterators, num_active))
            yield from map(next, iterators)

    def __init__(self, producers:list[Producer]) -> None:
        self.producers = producers
        super().__init__()