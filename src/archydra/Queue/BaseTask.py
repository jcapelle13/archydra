from dataclasses import asdict, dataclass


@dataclass
class BaseTask:
    action: str
    url: str
    dest: str

    def to_dict(self):
        return asdict(self)