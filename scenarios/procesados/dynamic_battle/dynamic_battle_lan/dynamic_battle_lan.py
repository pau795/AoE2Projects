import os
import shutil
from pathlib import Path

from data_mods.procesados.dynamic_battle_lan.dynamic_battle_lan import DynamicBattleLan
from scenarios.lib import utils
from scenarios.procesados.dynamic_battle.alcatraz.alcatraz import Alcatraz
from scenarios.procesados.dynamic_battle.armageddon.armageddon import Armageddon
from scenarios.procesados.dynamic_battle.earthquake.all_map_earthquake import Earthquake
from scenarios.procesados.dynamic_battle.earthquake.migration_earthaquake import EarthquakeMigration
from scenarios.procesados.dynamic_battle.enchanted_forest.enchanted_forest import EnchantedForest
from scenarios.procesados.dynamic_battle.fog.fog import Fog
from scenarios.procesados.dynamic_battle.jumanji.jumanji import Jumanji
from scenarios.procesados.dynamic_battle.maze_runner.maze_runer import MazeRunner
from scenarios.procesados.dynamic_battle.pirates_of_the_caribbean.pirates_of_the_caribbean import PiratesOfTheCaribbean
from scenarios.procesados.dynamic_battle.plague.plague import Plague
from scenarios.procesados.dynamic_battle.three_gorges.three_gorges import ThreeGorges
from scenarios.procesados.dynamic_battle.tsunami.fukushima import Fukushima
from scenarios.procesados.dynamic_battle.tsunami.tsunami import Tsunami
from scenarios.procesados.dynamic_battle.twister.twister import Twister
from scenarios.procesados.dynamic_battle.vulkan.vulkan_nomad import VulkanNomad
from scenarios.procesados.dynamic_battle.west_train.west_train import WestTrain

if __name__ == '__main__':
    steam_id = os.getenv('steam_id', 0)
    user_folder = Path(f'{os.environ["USERPROFILE"]}')

    scenario_folder = user_folder / 'Games' / 'Age of Empires 2 DE' / str(steam_id) / 'resources' / '_common' / 'scenario'
    output_folder = Path('Dynamic Battle LAN Maps')
    edit_maps_folder = output_folder / 'Edit Maps'
    output_maps_folder = output_folder / 'Output Maps'
    mod_maps_folder = output_folder / 'Mod Maps'
    dat_folder = output_folder / 'Dat File'

    zip_name = 'Dynamic_Battle_LAN_Map_Pack.zip'
    input_scenario_prefix = 'EDIT_'
    output_scenario_prefix = 'OUTPUT_'
    mod_scenario_prefix = 'DBL_'
    scenario_extension = '.aoe2scenario'

    alcatraz = 'ALCATRAZ_1V1'
    armageddon = 'ARMAGEDDON_1V1'
    earthquake = 'EARTHQUAKE_1V1'
    earthquake_migration = 'EARTHQUAKE_MIGRATION_1V1'
    enchanted_forest = 'ENCHANTED_FOREST_1V1'
    fog = 'FOG_1V1'
    fukushima = 'FUKUSHIMA_1V1'
    jumanji = 'JUMANJI_1V1'
    maze_runner = 'MAZE_RUNNER_1V1'
    pirates_of_the_caribbean = 'PIRATES_OF_THE_CARIBBEAN_1V1'
    plague = 'PLAGUE_1V1'
    three_gorges = 'THREE_GORGES_1V1'
    tsunami = 'TSUNAMI_1V1'
    twister = 'TWISTER_1V1'
    vulkan_nomad = 'VULKAN_NOMAD_1V1'
    west_train = 'WILD_WEST_TRAIN_1V1'

    print("Converting Maps...")
    alcatraz_class = Alcatraz(input_scenario_name=f'{input_scenario_prefix}{alcatraz}', output_scenario_name=f'{output_scenario_prefix}{alcatraz}')
    armageddon_class = Armageddon(input_scenario_name=f'{input_scenario_prefix}{armageddon}', output_scenario_name=f'{output_scenario_prefix}{armageddon}')
    earthquake_class = Earthquake(input_scenario_name=f'{input_scenario_prefix}{earthquake}', output_scenario_name=f'{output_scenario_prefix}{earthquake}')
    earthquake_migration_class = EarthquakeMigration(input_scenario_name=f'{input_scenario_prefix}{earthquake_migration}', output_scenario_name=f'{output_scenario_prefix}{earthquake_migration}')
    enchanted_forest_class = EnchantedForest(input_scenario_name=f'{input_scenario_prefix}{enchanted_forest}', output_scenario_name=f'{output_scenario_prefix}{enchanted_forest}')
    fog_class = Fog(input_scenario_name=f'{input_scenario_prefix}{fog}', output_scenario_name=f'{output_scenario_prefix}{fog}')
    fukushima_class = Fukushima(input_scenario_name=f'{input_scenario_prefix}{fukushima}', output_scenario_name=f'{output_scenario_prefix}{fukushima}')
    jumanji_class = Jumanji(input_scenario_name=f'{input_scenario_prefix}{jumanji}', output_scenario_name=f'{output_scenario_prefix}{jumanji}')
    maze_runner_class = MazeRunner(input_scenario_name=f'{input_scenario_prefix}{maze_runner}', output_scenario_name=f'{output_scenario_prefix}{maze_runner}')
    pirates_of_the_caribbean_class = PiratesOfTheCaribbean(input_scenario_name=f'{input_scenario_prefix}{pirates_of_the_caribbean}', output_scenario_name=f'{output_scenario_prefix}{pirates_of_the_caribbean}')
    plague_class = Plague(input_scenario_name=f'{input_scenario_prefix}{plague}', output_scenario_name=f'{output_scenario_prefix}{plague}')
    three_gorges_class = ThreeGorges(input_scenario_name=f'{input_scenario_prefix}{three_gorges}', output_scenario_name=f'{output_scenario_prefix}{three_gorges}')
    tsunami_class = Tsunami(input_scenario_name=f'{input_scenario_prefix}{tsunami}', output_scenario_name=f'{output_scenario_prefix}{tsunami}')
    twister_class = Twister(input_scenario_name=f'{input_scenario_prefix}{twister}', output_scenario_name=f'{output_scenario_prefix}{twister}')
    vulkan_nomad_class = VulkanNomad(input_scenario_name=f'{input_scenario_prefix}{vulkan_nomad}', output_scenario_name=f'{output_scenario_prefix}{vulkan_nomad}')
    west_train_class = WestTrain(input_scenario_name=f'{input_scenario_prefix}{west_train}', output_scenario_name=f'{output_scenario_prefix}{west_train}')

    alcatraz_class.convert()
    armageddon_class.convert()
    earthquake_class.convert()
    earthquake_migration_class.convert()
    enchanted_forest_class.convert()
    fog_class.convert()
    fukushima_class.convert()
    jumanji_class.convert()
    maze_runner_class.convert()
    pirates_of_the_caribbean_class.convert()
    plague_class.convert()
    three_gorges_class.convert()
    tsunami_class.convert()
    twister_class.convert()
    vulkan_nomad_class.convert()
    west_train_class.convert()

    print("Generating DAT File...")
    dynamic_battle_lan_dat = DynamicBattleLan(dat_folder)
    dynamic_battle_lan_dat.convert()

    print("Copying Maps...")
    shutil.copy(scenario_folder / f'{input_scenario_prefix}{alcatraz}{scenario_extension}', edit_maps_folder)
    shutil.copy(scenario_folder / f'{input_scenario_prefix}{armageddon}{scenario_extension}', edit_maps_folder)
    shutil.copy(scenario_folder / f'{input_scenario_prefix}{earthquake}{scenario_extension}', edit_maps_folder)
    shutil.copy(scenario_folder / f'{input_scenario_prefix}{earthquake_migration}{scenario_extension}', edit_maps_folder)
    shutil.copy(scenario_folder / f'{input_scenario_prefix}{enchanted_forest}{scenario_extension}', edit_maps_folder)
    shutil.copy(scenario_folder / f'{input_scenario_prefix}{fog}{scenario_extension}', edit_maps_folder)
    shutil.copy(scenario_folder / f'{input_scenario_prefix}{fukushima}{scenario_extension}', edit_maps_folder)
    shutil.copy(scenario_folder / f'{input_scenario_prefix}{jumanji}{scenario_extension}', edit_maps_folder)
    shutil.copy(scenario_folder / f'{input_scenario_prefix}{maze_runner}{scenario_extension}', edit_maps_folder)
    shutil.copy(scenario_folder / f'{input_scenario_prefix}{pirates_of_the_caribbean}{scenario_extension}', edit_maps_folder)
    shutil.copy(scenario_folder / f'{input_scenario_prefix}{plague}{scenario_extension}', edit_maps_folder)
    shutil.copy(scenario_folder / f'{input_scenario_prefix}{three_gorges}{scenario_extension}', edit_maps_folder)
    shutil.copy(scenario_folder / f'{input_scenario_prefix}{three_gorges}_LAYERS{scenario_extension}', edit_maps_folder)
    shutil.copy(scenario_folder / f'{input_scenario_prefix}{tsunami}{scenario_extension}', edit_maps_folder)
    shutil.copy(scenario_folder / f'{input_scenario_prefix}{twister}{scenario_extension}', edit_maps_folder)
    shutil.copy(scenario_folder / f'{input_scenario_prefix}{vulkan_nomad}{scenario_extension}', edit_maps_folder)
    shutil.copy(scenario_folder / f'{input_scenario_prefix}{west_train}{scenario_extension}', edit_maps_folder)

    shutil.copy(scenario_folder / f'{output_scenario_prefix}{alcatraz}{scenario_extension}', output_maps_folder)
    shutil.copy(scenario_folder / f'{output_scenario_prefix}{armageddon}{scenario_extension}', output_maps_folder)
    shutil.copy(scenario_folder / f'{output_scenario_prefix}{earthquake}{scenario_extension}', output_maps_folder)
    shutil.copy(scenario_folder / f'{output_scenario_prefix}{earthquake_migration}{scenario_extension}', output_maps_folder)
    shutil.copy(scenario_folder / f'{output_scenario_prefix}{enchanted_forest}{scenario_extension}', output_maps_folder)
    shutil.copy(scenario_folder / f'{output_scenario_prefix}{fog}{scenario_extension}', output_maps_folder)
    shutil.copy(scenario_folder / f'{output_scenario_prefix}{fukushima}{scenario_extension}', output_maps_folder)
    shutil.copy(scenario_folder / f'{output_scenario_prefix}{jumanji}{scenario_extension}', output_maps_folder)
    shutil.copy(scenario_folder / f'{output_scenario_prefix}{maze_runner}{scenario_extension}', output_maps_folder)
    shutil.copy(scenario_folder / f'{output_scenario_prefix}{pirates_of_the_caribbean}{scenario_extension}', output_maps_folder)
    shutil.copy(scenario_folder / f'{output_scenario_prefix}{plague}{scenario_extension}', output_maps_folder)
    shutil.copy(scenario_folder / f'{output_scenario_prefix}{three_gorges}{scenario_extension}', output_maps_folder)
    shutil.copy(scenario_folder / f'{output_scenario_prefix}{tsunami}{scenario_extension}', output_maps_folder)
    shutil.copy(scenario_folder / f'{output_scenario_prefix}{twister}{scenario_extension}', output_maps_folder)
    shutil.copy(scenario_folder / f'{output_scenario_prefix}{vulkan_nomad}{scenario_extension}', output_maps_folder)
    shutil.copy(scenario_folder / f'{output_scenario_prefix}{west_train}{scenario_extension}', output_maps_folder)

    shutil.copy(scenario_folder / f'{output_scenario_prefix}{alcatraz}{scenario_extension}', mod_maps_folder / f'{mod_scenario_prefix}{alcatraz}{scenario_extension}')
    shutil.copy(scenario_folder / f'{output_scenario_prefix}{armageddon}{scenario_extension}', mod_maps_folder / f'{mod_scenario_prefix}{armageddon}{scenario_extension}')
    shutil.copy(scenario_folder / f'{output_scenario_prefix}{earthquake}{scenario_extension}', mod_maps_folder / f'{mod_scenario_prefix}{earthquake}{scenario_extension}')
    shutil.copy(scenario_folder / f'{output_scenario_prefix}{earthquake_migration}{scenario_extension}', mod_maps_folder / f'{mod_scenario_prefix}{earthquake_migration}{scenario_extension}')
    shutil.copy(scenario_folder / f'{output_scenario_prefix}{enchanted_forest}{scenario_extension}', mod_maps_folder / f'{mod_scenario_prefix}{enchanted_forest}{scenario_extension}')
    shutil.copy(scenario_folder / f'{output_scenario_prefix}{fog}{scenario_extension}', mod_maps_folder / f'{mod_scenario_prefix}{fog}{scenario_extension}')
    shutil.copy(scenario_folder / f'{output_scenario_prefix}{fukushima}{scenario_extension}', mod_maps_folder / f'{mod_scenario_prefix}{fukushima}{scenario_extension}')
    shutil.copy(scenario_folder / f'{output_scenario_prefix}{jumanji}{scenario_extension}', mod_maps_folder / f'{mod_scenario_prefix}{jumanji}{scenario_extension}')
    shutil.copy(scenario_folder / f'{output_scenario_prefix}{maze_runner}{scenario_extension}', mod_maps_folder / f'{mod_scenario_prefix}{maze_runner}{scenario_extension}')
    shutil.copy(scenario_folder / f'{output_scenario_prefix}{pirates_of_the_caribbean}{scenario_extension}', mod_maps_folder / f'{mod_scenario_prefix}{pirates_of_the_caribbean}{scenario_extension}')
    shutil.copy(scenario_folder / f'{output_scenario_prefix}{plague}{scenario_extension}', mod_maps_folder / f'{mod_scenario_prefix}{plague}{scenario_extension}')
    shutil.copy(scenario_folder / f'{output_scenario_prefix}{three_gorges}{scenario_extension}', mod_maps_folder / f'{mod_scenario_prefix}{three_gorges}{scenario_extension}')
    shutil.copy(scenario_folder / f'{output_scenario_prefix}{tsunami}{scenario_extension}', mod_maps_folder / f'{mod_scenario_prefix}{tsunami}{scenario_extension}')
    shutil.copy(scenario_folder / f'{output_scenario_prefix}{twister}{scenario_extension}', mod_maps_folder / f'{mod_scenario_prefix}{twister}{scenario_extension}')
    shutil.copy(scenario_folder / f'{output_scenario_prefix}{vulkan_nomad}{scenario_extension}', mod_maps_folder / f'{mod_scenario_prefix}{vulkan_nomad}{scenario_extension}')
    shutil.copy(scenario_folder / f'{output_scenario_prefix}{west_train}{scenario_extension}', mod_maps_folder / f'{mod_scenario_prefix}{west_train}{scenario_extension}')

    print("Zipping folder...")
    utils.zip_folder(output_folder, zip_name)
