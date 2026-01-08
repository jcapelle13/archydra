VALID_CONSUMERS = {}

from .BaseConsumer import BaseConsumer as BaseConsumer
from .LoggingConsumer import LoggingConsumer as LoggingConsumer
from .ReadWiseConsumer import ReadWiseConsumer as ReadWiseConsumer

VALID_CONSUMERS = {
    "ReadWiseConsumer": ReadWiseConsumer,
    "LoggingConsumer": LoggingConsumer,
}
