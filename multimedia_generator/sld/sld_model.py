from dataclasses import dataclass
from io import BytesIO

from PIL import Image
from numpy import ndarray


@dataclass
class SLDHeader:
    format: str
    version: int
    frames: int
    unknown1: int
    opacity: int


@dataclass
class SLDLayerData:
    coordinates: list
    inherited: bool
    image_data: ndarray


@dataclass
class SLDFrameData:
    normal: SLDLayerData = None
    shadow: SLDLayerData = None
    unknown: BytesIO = None
    smudge: BytesIO = None
    player: SLDLayerData = None


@dataclass
class SLDFrame:
    width: int
    height: int
    anchorX: int
    anchorY: int
    frameType: int
    unknown: int
    index: int
    data: SLDFrameData


@dataclass
class SLDSprite:
    header: SLDHeader
    frames: list[SLDFrame]
