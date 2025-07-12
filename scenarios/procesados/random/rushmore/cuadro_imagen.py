import itertools

from AoE2ScenarioParser.datasets.terrains import TerrainId
from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario
from PIL import Image
import os


def check_bad_elevations(map_manager, tile):
    found = False
    for dx, dy in itertools.product((-1, 0, 1), repeat=2):
        if (dx == 0 and dy == 0) or not (0 <= tile.x + dx < map_manager.map_width) or not (0 <= tile.y + dy < map_manager.map_height):
            continue
        new_tile = map_manager.get_tile(tile.x + dx, tile.y + dy)
        difference = abs(tile.elevation - new_tile.elevation)
        if difference > 1:
            found = True
    if found:
        print(f'tile {tile.x}, {tile.y}, ELEVATION -> {tile.elevation}')
        for dx, dy in itertools.product((-1, 0, 1), repeat=2):
            if (dx == 0 and dy == 0) or not (0 <= tile.x + dx < map_manager.map_width) or not (0 <= tile.y + dy < map_manager.map_height):
                continue
            print(f'   Adjacent {tile.x + dx}, {tile.y + dy}, ELEVATION -> {map_manager.get_tile(tile.x + dx, tile.y + dy).elevation}')


user_folder = f'{os.environ["USERPROFILE"]}'
steam_id = os.getenv('steam_id', 0)
scenario_folder = f'{user_folder}\\Games\\Age of Empires 2 DE\\{steam_id}\\resources\\_common\\scenario\\'

scenario_name = 'rushmore'
input_file = f'{scenario_folder}{scenario_name}.aoe2scenario'
output_file = f'{scenario_folder}{scenario_name}_imagen.aoe2scenario'
image_folder = "imagenes/rushmore_8p_isometric.png"
csv = "imagenes/elevation.csv"


terrains = [TerrainId.GRAVEL_DESERT, TerrainId.ROAD_GRAVEL, TerrainId.GRAVEL_DEFAULT, TerrainId.BEACH_WET_GRAVEL]

image = Image.open(image_folder).convert("RGBA")
scenario = AoE2DEScenario.from_file(input_file)
unit_manger = scenario.unit_manager
map_manager = scenario.map_manager

canvas_center = (map_manager.map_width - image.width // 2 - 10, image.height // 2 + 10)
canvas_area = scenario.new.area()
canvas_area.center(canvas_center[0], canvas_center[1]).width(image.width).height(image.height)
canvas_corner = canvas_area.corner1

tiles_by_color = {}

for x in range(image.width):
    for y in range(image.height):
        pixel = image.getpixel((x, y))
        if pixel[3] != 0:
            color = (pixel[0], pixel[1], pixel[2])
            tile = map_manager.get_tile(canvas_corner.x + x, canvas_corner.y + y)
            if color not in tiles_by_color:
                tiles_by_color[color] = []
            tiles_by_color[color].append(tile)


ordered_colors = sorted(list(tiles_by_color.keys()), reverse=True, key=lambda c: c[0] + c[1] + c[2])
for i, color in enumerate(ordered_colors):
    for tile in tiles_by_color[color]:
        tile.terrain_id = terrains[i]
        if 0 <= tile.x + 1 < map_manager.map_width and 0 <= tile.y + 1 < map_manager.map_height:
            map_manager.set_elevation(15, tile.x, tile.y, tile.x + 1, tile.y + 1)

map_manager.get_tile(199, 106).elevation = 11
map_manager.get_tile(197, 111).elevation = 13
map_manager.get_tile(200, 106).elevation = 11
map_manager.get_tile(239, 108).elevation = 2

for tile in scenario.new.area().select_entire_map().to_coords(as_terrain=True):
    if tile.elevation == 0:
        tile.terrain_id = TerrainId.GRASS_OTHER
    check_bad_elevations(map_manager, tile)

with open(csv, "w", encoding="utf-8") as f:
    for x in range(map_manager.map_width):
        line = ""
        for y in range(map_manager.map_height):
            line += f'{map_manager.get_tile(x, y).elevation};'
        f.write(f'{line}\n')

scenario.write_to_file(output_file)
