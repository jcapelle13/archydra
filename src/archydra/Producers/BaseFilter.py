from typing import Iterable
from loguru import logger
from ..Helpers import roundrobin, VALID_PRODUCERS
from . import BaseProducer


class BaseFilter(BaseProducer):
    """
    Special kind of producer that takes in other producers as input
    """

    def _roundrobin(self):
        logger.debug("Starting roundrobin")
        yield from roundrobin(*(p.get_urls() for p in self.producers))

    def __init__(self, producers: Iterable[BaseProducer|dict]) -> None:
        self.producers = [ BaseProducer.from_config(p) if isinstance(p,dict) else p for p in producers ]
        super().__init__()
