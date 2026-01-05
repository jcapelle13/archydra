from archydra.Queue.BaseTask import BaseTask
from .BaseQueue import BaseQueue
from pathlib import Path
from os import PathLike
from loguru import logger

class FSQueue(BaseQueue):
    """
    FileSystem-based Queue
    """
    def __init__(self, base_dir:Path|str|PathLike, add_gitignore=True) -> None:
        super().__init__()
        logger.debug("Creating FSQueue at {}",base_dir)
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
        if add_gitignore:
            logger.debug("Creating gitignore...")
            gitignore = self.base_dir / ".gitignore"
            gitignore.write_text("*\n")
    
    def enqueue(self, t: BaseTask):
        time_stamp = "ts"
        task_file = self.base_dir / f"task-{time_stamp}.txt"
        logger.debug("Writing task to {}",task_file)
        task_file.write_text("\n".join([t.url,t.dest]))
    
    def dequeue(self) -> BaseTask | None:
        if len(self) == 0:
            logger.warning("Queue in {} is empty!",self.base_dir)
            return None
        oldest_task = min(self.base_dir.glob("*.txt"))
        logger.debug("Read task from {}",oldest_task)
        txt = oldest_task.read_text()
        new_task = BaseTask(*txt.split("\n"))
        # in pathlib, unlink() deletes a file or removes a symlink
        oldest_task.unlink()
        return new_task

    def __len__(self) -> int:
        return len(list(self.base_dir.glob("*.txt")))