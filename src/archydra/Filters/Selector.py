from typing import Iterable
from archydra.AbstractClasses import Filter, Producer
from itertools import islice
from loguru import logger

class Selector(Filter):
    """
    Filter that only outputs urls that user selects
    """
    def __init__(self, producers: list[Producer], page_size=2) -> None:
        super().__init__(producers)
        self.page_size = page_size

    def get_urls(self) -> Iterable[str]:
        rr_gen = self._roundrobin()
        while True:
            current_page = list(islice(rr_gen,self.page_size))
            if current_page:
                for line_num in range(len(current_page)):
                    print(f"{line_num} - {current_page[line_num]}")
                wanted = [int(x) for x in input("Enter wanted items: ").split(",")]
                logger.debug("Selected: {}",wanted)
                for x in wanted:
                    yield current_page[x]
            else:
                break