from abc import ABC, abstractmethod


class BaseConsumer(ABC):
    @abstractmethod
    def process_url(self, url: str) -> None:
        """
        Process a URL

        :param url: Description
        :type url: str
        """
        pass
