from dataclasses import dataclass


@dataclass
class Video:
    name: str
    filepath: str
    current_timing: float
    paused: bool

    def update_video(self, name: str, filepath: str, current_timing: str, paused: bool):
        self.name = name
        self.filepath = filepath
        self.current_timing = current_timing
        self.paused = paused