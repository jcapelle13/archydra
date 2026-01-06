from .BaseProducer import BaseProducer
from pathlib import Path
from os import PathLike
from loguru import logger


class FileProducer(BaseProducer):
    def __init__(self, file_path:Path|PathLike|str, create_file=True):
        logger.debug(f"Creating FileProducer from: {file_path}")
        self.file_path = Path(file_path)
        if not self.file_path.exists() and create_file:
            self.file_path.touch()
        super().__init__()

    def get_urls(self):
        logger.debug("Opening file: {}", self.file_path)
        if not self.file_path.exists():
            raise FileNotFoundError(f"{self.file_path} not found")
        with open(self.file_path) as f:
            for line in f:
                yield line.strip()
