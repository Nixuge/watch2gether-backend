from dataclasses import dataclass


@dataclass
class Video:
    name: str
    filepath: str
    current_timing: float
    paused: bool
