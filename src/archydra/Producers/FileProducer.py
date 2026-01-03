from archydra.AbstractClasses import Producer
from pathlib import Path
from loguru import logger

class FileProducer(Producer):
    def __init__(self, path:Path):
        self.path = path
        super().__init__()
    
    def get_urls(self):
        logger.debug("Opening file: {}", self.path)
        with open(self.path) as f:
            for line in f:
                yield line