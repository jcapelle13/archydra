from abc import ABC, abstractmethod
from hashlib import blake2b
from itertools import cycle, islice
from pathlib import Path
from typing import Iterable

from loguru import logger
from ruamel.yaml import YAML

from .Queue import *

yaml = YAML()



class Worker(ABC):
    task_queue: BaseQueue
    config: dict

    def __init__(self, config_path: Path) -> None:
        self.worker_name = (
            f"{self.__class__.__name__}-{blake2b(digest_size=4).hexdigest()}"
        )
        logger.debug(f"Instantiating {self.__class__.__name__} with {config_path}")
        with open(config_path) as conf_file:
            self.config = yaml.load(conf_file)
        queue_type = self.config["queue_type"]
        if queue_type not in QUEUE_TYPES:
            raise ValueError(f"{queue_type} is not a supported Queue Type")
        queue_class: type = QUEUE_TYPES[queue_type]
        if not issubclass(queue_class, BaseQueue):
            raise ValueError(
                f"{queue_type} is in the list of supported queues, but not a subclass of BaseQueue"
            )
        queue_args: dict = self.config.get("queue_args", {})
        self.task_queue = queue_class(**queue_args)

    @abstractmethod
    async def start(self) -> None:
        pass


def roundrobin[T](*iterables: Iterable[T]):
    "Visit input iterables in a cycle until each is exhausted."
    # roundrobin('ABC', 'D', 'EF') → A D E B F C
    # Algorithm credited to George Sakkis
    iterators = map(iter, list(iterables))
    for num_active in range(len(iterables), 0, -1):
        iterators = cycle(islice(iterators, num_active))
        yield from map(next, iterators)

from .Consumers import *
from .Producers import *
