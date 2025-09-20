import json
import math
from pathlib import Path

from AoE2ScenarioParser.objects.data_objects.terrain_tile import TerrainTile
from AoE2ScenarioParser.objects.managers.map_manager import MapManager
from AoE2ScenarioParser.objects.support.area import Area
from AoE2ScenarioParser.objects.support.tile import Tile
from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario


def get_edge_tile(map_manager: MapManager, tile: Tile, direction: tuple[int, int]) -> TerrainTile:
    """Get the edge tile in the given direction from the given tile.

    Args:
        map_manager (MapManager): The scenario map manager.
        tile (Tile): The initial tile.
        direction (tuple[int, int]): The direction from the initial tile.

    Returns:
        TerrainTile: The edge tile in the given direction.
    """
    x, y = tile
    while 0 <= x < map_manager.map_width and 0 <= y < map_manager.map_height:
        x += direction[0]
        y += direction[1]
    x = int(x - direction[0])
    y = int(y - direction[1])
    return map_manager.get_tile(int(x), int(y))


def get_direction(tile1: Tile, tile2: Tile) -> tuple[int, int]:
    difference = (tile2.x - tile1.x, tile2.y - tile1.y)
    length = math.hypot(difference[0], difference[1])
    return int(difference[0] / length), int(difference[1] / length)


def modify_area_dimension(area: Area, short_or_long: str, shrink_or_expand: str, n: int):
    dimension = area.get_width() < area.get_height()
    axis = short_or_long == 'long'
    if shrink_or_expand == 'shrink':
        if dimension == axis:
            area.shrink_y1(n)
            area.shrink_y2(n)
        else:
            area.shrink_x1(n)
            area.shrink_x2(n)
    elif shrink_or_expand == 'expand':
        if dimension == axis:
            area.expand_y1(n)
            area.expand_y2(n)
        else:
            area.expand_x1(n)
            area.shrink_x2(n)
    return area


def get_terrain_dict():
    module_dir = Path(__file__).parent
    terrain_dict_file = module_dir / "data/terrains.json"
    with open(terrain_dict_file, 'r') as f:
        dict1 = {}
        terrain_dict = json.load(f)
        for terrain, value in terrain_dict.items():
            dict1[int(terrain)] = value
        return dict1


def get_terrain_restrictions():
    module_dir = Path(__file__).parent
    terrain_dict_file = module_dir / "data/terrain_restrictions.json"
    with open(terrain_dict_file, 'r') as f:
        dict1 = {}
        terrain_dict = json.load(f)
        for restriction, value in terrain_dict.items():
            dict1[int(restriction)] = value
        return dict1
