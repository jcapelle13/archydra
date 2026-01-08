VALID_PRODUCERS = {}

from .BaseProducer import BaseProducer as BaseProducer
from .FileProducer import FileProducer as FileProducer

VALID_PRODUCERS = {"FileProducer": FileProducer}