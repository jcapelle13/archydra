from archydra.Abstracts import Producer
from pathlib import Path

class FileProducer(Producer):
    def __init__(self, path:Path):
        self.path = path
        super().__init__()
    
    def get_urls(self):
        with open(self.path) as f:
            for line in f:
                yield line