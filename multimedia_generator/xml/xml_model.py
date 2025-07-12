from dataclasses import dataclass


@dataclass
class DatabaseUnit:
    id: int
    data_id: int
    name: str
    image: str
    gif: str
