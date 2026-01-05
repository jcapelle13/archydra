from dataclasses import dataclass


@dataclass
class BaseTask:
    url: str
    dest: str
