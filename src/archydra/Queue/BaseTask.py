from dataclasses import dataclass, asdict


@dataclass
class BaseTask:
    action: str
    url: str
    dest: str

    def to_dict(self):
        return asdict(self)