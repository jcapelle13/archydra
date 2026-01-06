from abc import abstractmethod
from pathlib import Path
from ..Helpers import Worker, VALID_CONSUMERS
from loguru import logger
from asyncio import sleep

CONSUMER_PATH = Path("./etc/consumer.yaml")
SLEEP_SECS=10
class BaseConsumer(Worker):

    def __init__(self) -> None:
        super().__init__(CONSUMER_PATH)

    async def start(self) -> None:
        while len(self.task_queue) == 0:
            logger.info("No tasks! waiting for work...")
            logger.debug("Sleeping for {} seconds.",SLEEP_SECS)
            await sleep(SLEEP_SECS)
            
        while len(self.task_queue) > 0:
            new_task = await self.task_queue.dequeue()
            logger.debug(f"new task: {new_task}")
            if new_task is None:
                logger.critical("Race condition! Ran out of taks before ending the list")
                break
            self.process_url(new_task.url)

    @abstractmethod
    def process_url(self, url: str) -> None:
        """
        Process a URL

        :param url: Description
        :type url: str
        """
        pass

    @classmethod
    def from_config(cls, config:dict) -> 'BaseConsumer':
        con_type = config.get('type')
        if con_type not in VALID_CONSUMERS:
            raise ValueError(f"{con_type} is not a valid Consumer Type")
        con_class:type = VALID_CONSUMERS[con_type]
        if not issubclass(con_class, BaseConsumer):
            raise ValueError(f"{con_type} is a valid, but {con_class} is not a subclass of BaseConsumer")
        con_args = config.get("args",{})
        return con_class(**con_args)
