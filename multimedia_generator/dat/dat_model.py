from dataclasses import dataclass


@dataclass
class GraphicDelta:
    graphic_id: int
    offset_x: int
    offset_y: int


@dataclass
class GraphicData:
    id: int
    sprite_file: str
    frames_per_angle: int
    frame_duration: float
    mirror_mode: int
    deltas: list[GraphicDelta]


@dataclass
class UnitData:
    id: int
    name_string_id: int
    icon_id: int
    reload_time: float
    standing_graphic: GraphicData = None
    dying_graphic: GraphicData = None
    walking_graphic: GraphicData = None
    attack_graphic: GraphicData = None
    idle_attack_graphic: GraphicData = None

