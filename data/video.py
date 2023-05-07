from dataclasses import dataclass


@dataclass
class Video:
    name: str
    src: str
    time: float
    paused: bool
