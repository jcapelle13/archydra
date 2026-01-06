from datetime import datetime
from os import PathLike
from pathlib import Path

from loguru import logger
from ruamel.yaml import YAML

from .BaseQueue import BaseQueue
from .BaseTask import BaseTask

yaml = YAML()


class FSQueue(BaseQueue):
    """
    FileSystem-based Queue
    """

    def __init__(self, base_dir: Path | str | PathLike, add_gitignore=True) -> None:
        super().__init__()
        logger.debug("Creating FSQueue at {}", base_dir)
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
        if add_gitignore:
            logger.debug("Creating gitignore...")
            gitignore = self.base_dir / ".gitignore"
            gitignore.write_text("*\n")

    async def enqueue(self, t: BaseTask):
        time_stamp = f"{datetime.now().timestamp()}"
        task_file = self.base_dir / f"task-{time_stamp}.txt"
        logger.debug("Writing task to {}", task_file)
        with open(task_file, "w") as new_file:
            yaml.dump(t.to_dict(), new_file)

    async def dequeue(self) -> BaseTask | None:
        if len(self) == 0:
            logger.warning("Filesystem Queue in {} is empty!", self.base_dir)
            return None
        oldest_task = min(self.base_dir.glob("*.txt"))
        logger.debug("Read task from {}", oldest_task)
        with open(oldest_task) as task_file:
            data = yaml.load(task_file)
            logger.trace(f"data from {oldest_task}: {data}")
            new_task = BaseTask(**data)
        # in pathlib, unlink() deletes a file or removes a symlink
        oldest_task.unlink()
        return new_task

    def __len__(self) -> int:
        return len(list(self.base_dir.glob("*.txt")))
