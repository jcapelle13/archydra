import os
from itertools import islice
from typing import Iterable

import click
from loguru import logger

from . import BaseProducer
from .BaseFilter import BaseFilter


class Selector(BaseFilter):
    """
    Filter that only outputs urls that user selects
    """

    def __init__(self, producers: list[BaseProducer|dict], page_size=0) -> None:
        super().__init__(producers)
        if page_size > 0:
            self.page_size = page_size
        else:
            window_size = os.get_terminal_size()
            logger.trace("Terminal size: {}", window_size)
            self.page_size = window_size.lines - 3
        logger.debug("Set page size to {}", self.page_size)

    def get_urls(self) -> Iterable[str]:
        rr_gen = self._roundrobin()
        while True:
            current_page = list(islice(rr_gen, self.page_size))
            if current_page:
                for line_num in range(len(current_page)):
                    click.echo(f"{line_num} - {current_page[line_num]}")
                wanted = [int(x) for x in click.prompt("Enter wanted items").split(",")]
                logger.debug("Selected: {}", wanted)
                for x in wanted:
                    yield current_page[x]
            else:
                break
