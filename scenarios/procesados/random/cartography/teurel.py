import itertools
from pathlib import Path

from AoE2ScenarioParser.datasets.terrains import TerrainId
from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario
from PIL import Image
import os


def get_scenario_tile(map_width, map_height, image_width, image_height, i, j):
    return int(i / image_width * map_width), int(j / image_height * map_height)


user_folder = f'{os.environ["USERPROFILE"]}'
steam_id = os.getenv('steam_id', 0)
scenario_folder = f'{user_folder}\\Games\\Age of Empires 2 DE\\{steam_id}\\resources\\_common\\scenario\\'

scenario_name = 'teruel'
input_file = f'{scenario_folder}{scenario_name}.aoe2scenario'
output_file = f'{scenario_folder}{scenario_name}_imagen.aoe2scenario'
image_path = Path("imagenes/teruel_borde_iso.png")
outer_terrain = TerrainId.DIRT_MUD

image = Image.open(image_path).convert("RGBA")
scenario = AoE2DEScenario.from_file(input_file)
unit_manger = scenario.unit_manager
map_manager = scenario.map_manager


for x in range(image.width):
    for y in range(image.height):
        pixel = image.getpixel((x, y))
        if pixel[3] == 0:
            tile_x, tile_y = get_scenario_tile(map_manager.map_width, map_manager.map_height, image.width, image.height, x, y)
            map_manager.get_tile(tile_x, tile_y).terrain_id = outer_terrain


scenario.write_to_file(output_file)
