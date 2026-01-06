from abc import abstractmethod
from typing import Iterable
from pathlib import Path
from ruamel.yaml import YAML
from ..Helpers import Worker
from ..Queue import BaseTask
from loguru import logger
yaml = YAML()


PRODUCER_CONFIG = Path("./etc/producer.yaml")


class BaseProducer(Worker):
    def __init__(self) -> None:
        super().__init__(PRODUCER_CONFIG)
    
    async def start(self) -> None:
        logger.info(f"{self.worker_name} is starting...")
        for url in self.get_urls():
            new_task = BaseTask(url=url, action="Download",dest="./tmp")
            await self.task_queue.enqueue(new_task)
        logger.info(f"{self.worker_name} is done!")

        

    @abstractmethod
    def get_urls(self) -> Iterable[str]:
        """
        Get the URLs from the producer

        :return: An Iterable of strings
        :rtype: Iterable[str]
        """
        pass
