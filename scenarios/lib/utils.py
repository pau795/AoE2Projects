import json
import math
import shutil
import tempfile
import zipfile
from pathlib import Path

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


def parametrize_xs(xs_file_path: Path, parameters: dict[str, str]):
    with open(xs_file_path, 'r') as xs_file:
        xs_content = xs_file.read()
        for key, value in parameters.items():
            xs_content = xs_content.replace(f'{{{{{key}}}}}', value)
        return xs_content


def zip_folder(source_dir: Path, archive_name: str):
    source_dir = source_dir.resolve()
    if not source_dir.is_dir():
        raise ValueError(f"{source_dir} is not a valid directory")

    # Prepare the output path
    final_zip_path = source_dir / archive_name

    # If it already exists, remove it to avoid shutil.move error
    if final_zip_path.exists():
        final_zip_path.unlink()

    # Temporary zip path (outside the source dir)
    temp_zip_path = Path(tempfile.gettempdir()) / archive_name

    # Ensure no leftover from previous runs
    if temp_zip_path.exists():
        temp_zip_path.unlink()

    # Create the zip with filtering
    with zipfile.ZipFile(temp_zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in source_dir.rglob('*'):
            if file_path.is_file() and file_path.name.lower() != 'desktop.ini':
                relative_path = file_path.relative_to(source_dir)
                zipf.write(file_path, arcname=relative_path)

    # Move the zip back to the source folder
    shutil.move(str(temp_zip_path), str(final_zip_path))

    print(f"✅ Zip created at: {final_zip_path}")