from AoE2ScenarioParser.objects.data_objects.terrain_tile import TerrainTile
from AoE2ScenarioParser.objects.managers.map_manager import MapManager
from AoE2ScenarioParser.objects.support.area import Area
from AoE2ScenarioParser.objects.support.tile import Tile


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


def increment_tile(tile: Tile, increment: tuple[int, int], step: int):
    return Tile(tile.x + increment[0] * step, tile.y + increment[1] * step)


def generate_range(x: int, y: int) -> list[int]:
    """Generate a list of numbers between x and y (inclusive).

    Args:
        x: First number
        y: Second number

    Returns:
        List of integers from x to y (inclusive), in ascending order.
    """
    step = 1 if x <= y else -1
    return list(range(x, y + step, step))


def set_area_coordinates(area: Area, x1: int, x2: int, y1: int, y2: int) -> Area:
    """
    Set the coordinates of the given area.

    Args:
        area (Area): The area to modify.
        x1 (int): The new x1 coordinate.
        x2 (int): The new x2 coordinate.
        y1 (int): The new y1 coordinate.
        y2 (int): The new y2 coordinate.

    Returns:
        Area: The modified area.
    """
    area.x1 = x1
    area.y1 = y1
    area.x2 = x2
    area.y2 = y2
    return area
