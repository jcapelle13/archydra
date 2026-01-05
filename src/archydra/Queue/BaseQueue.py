from abc import ABC, abstractmethod
from .BaseTask import BaseTask


class BaseQueue(ABC):
    @abstractmethod
    def enqueue(self, t: BaseTask):
        pass

    @abstractmethod
    def dequeue(self) -> BaseTask | None:
        pass

    @abstractmethod
    def __len__(self) -> int:
        pass