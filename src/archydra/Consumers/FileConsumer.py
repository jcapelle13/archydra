from . import BaseConsumer
from os import PathLike
from pathlib import Path

class FileConsumer(BaseConsumer):
    def __init__(self, file_name:str|PathLike|Path) -> None:
        self.dest_file = Path(file_name)
        super().__init__()
    
    def process_url(self, url: str) -> None:
        with open(self.dest_file,'a') as f:
            f.write(f"{url}\n")