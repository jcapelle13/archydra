from typing import Iterable
from loguru import logger
from archydra.Helpers import roundrobin
from archydra.Producers import _BaseProducer

class BaseFilter(_BaseProducer):
    """
    Special kind of producer that takes in other producers as input
    """

    def _roundrobin(self):
        logger.debug("Starting roundrobin")
        yield from roundrobin(*(p.get_urls() for p in self.producers))

    def __init__(self, producers: Iterable[_BaseProducer]) -> None:
        self.producers = producers
        super().__init__()
