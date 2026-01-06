from abc import ABC, abstractmethod

from .BaseTask import BaseTask


class BaseQueue(ABC):
    @abstractmethod
    async def enqueue(self, t: BaseTask):
        pass

    @abstractmethod
    async def dequeue(self) -> BaseTask | None:
        pass

    @abstractmethod
    def __len__(self) -> int:
        pass