from archydra.AbstractClasses import Consumer

from loguru import logger


class LoggingConsumer(Consumer):
    def __init__(self, log_level="DEBUG",) -> None:
        self.log_level = log_level
        super().__init__()

    def process_url(self, url: str) -> None:
        logger.log(self.log_level, "Got url:")
        return super().process_url(url)