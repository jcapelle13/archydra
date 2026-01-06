from abc import abstractmethod
from typing import Iterable
from pathlib import Path
from ruamel.yaml import YAML
from ..Helpers import Worker, VALID_PRODUCERS
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
    
    @classmethod
    def from_config(cls, config:dict) -> 'BaseProducer':
        prod_type = config.get('type')
        if prod_type not in VALID_PRODUCERS:
            raise ValueError(f"{prod_type} is not a valid Producer Type")
        prod_class:type = VALID_PRODUCERS[prod_type]
        if not issubclass(prod_class, BaseProducer):
            raise ValueError(f"{prod_type} is a valid, but {prod_class} is not a subclass of BaseProducer")
        prod_args = config.get("args",{})
        return prod_class(**prod_args)

        

    @abstractmethod
    def get_urls(self) -> Iterable[str]:
        """
        Get the URLs from the producer

        :return: An Iterable of strings
        :rtype: Iterable[str]
        """
        pass
