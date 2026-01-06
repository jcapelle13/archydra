from .BaseConsumer import BaseConsumer

from loguru import logger


class LoggingConsumer(BaseConsumer):
    def __init__(
        self,
        log_level="DEBUG",
    ) -> None:
        self.log_level = log_level
        super().__init__()

    def process_url(self, url: str) -> None:
        logger.log(self.log_level, f"Got url: {url}")
        