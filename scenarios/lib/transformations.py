import math

from AoE2ScenarioParser.objects.support.tile import Tile


def rotate_tile(tile: tuple[float, float], angle: float) -> tuple[float, float]:
    x_rot = (tile[0] * math.cos(angle)) - (tile[1] * math.sin(angle))
    y_rot = (tile[0] * math.sin(angle)) + (tile[1] * math.cos(angle))
    return x_rot, y_rot


def translate_tile(tile: tuple[float, float], translate: tuple[float, float]) -> tuple[float, float]:
    x_trans = tile[0] + translate[0]
    y_trans = tile[1] + translate[1]
    return x_trans, y_trans


def rotate_and_translate_tile(tile: tuple[float, float], angle: float, translate: tuple[float, float]) -> tuple[float, float]:
    tile = rotate_tile(tile, angle)
    tile = translate_tile(tile, translate)
    return tile


def get_tile(tile: tuple[float, float]) -> Tile:
    return Tile(int(tile[0]), int(tile[1]))


def line_formula(tile: tuple[float, float], vector: tuple[float, float]) -> (lambda x: float):
    m = vector[1] / vector[0]
    b = tile[1] - (m * tile[0])
    return lambda x: m * x + b
