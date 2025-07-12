from dataclasses import dataclass


@dataclass
class CSVUnitGif:
    id: int
    image: str
    animation: str
    ok: bool

@dataclass
class CSVBuildingGif:
    id1: int
    id2: int
    id3: int
    id4: int
    image: str
    animation: str
    ok: bool

@dataclass
class CSVUnitIcon:
    id: int
    image: int
