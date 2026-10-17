"""Speaker dataclass."""
from dataclasses import dataclass, field


@dataclass
class Speaker:
    name: str
    embedding: list = field(default_factory=list)
    timbre: list = field(default_factory=list)
    gender: str = "unknown"
    description: str = ""

    def as_dict(self):
        return {
            "name": self.name,
            "gender": self.gender,
            "description": self.description,
        }
