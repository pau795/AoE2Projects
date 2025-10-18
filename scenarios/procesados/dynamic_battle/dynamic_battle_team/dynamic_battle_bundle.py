import os
import shutil
from pathlib import Path

from scenarios.lib import utils
from scenarios.procesados.dynamic_battle.armageddon.armageddon_multiplayer import ArmageddonMultiplayer
from scenarios.procesados.dynamic_battle.enchanted_forest.enchanted_forest_multiplayer import EnchantedForestMultiplayer
from scenarios.procesados.dynamic_battle.catastrophic.castastrophic_multiplayer import CatastrophicMultiplayer
from scenarios.procesados.dynamic_battle.caves.caves_multiplayer import CavesMultiplayer
from scenarios.procesados.dynamic_battle.earthquake.earthquake_multiplayer import EarthquakeMultiplayer
from scenarios.procesados.dynamic_battle.fog.fog_multiplayer import FogMultiplayer
from scenarios.procesados.dynamic_battle.tsunami.tsunami_multiplayer import TsunamiMultiplayer
from scenarios.procesados.dynamic_battle.vulkan.vulkan_multiplayer import VulkanMultiplayer
from scenarios.procesados.dynamic_battle.west_train.west_train_mutliplayer import WestTrainMultiplayer


if __name__ == '__main__':
    steam_id = os.getenv('steam_id', 0)
    user_folder = Path(f'{os.environ["USERPROFILE"]}')

    scenario_folder = user_folder / 'Games' / 'Age of Empires 2 DE' / str(steam_id) / 'resources' / '_common' / 'scenario'
    output_folder = Path('Dynamic Battle Team Maps')
    edit_maps_folder = output_folder / 'Edit Maps'
    output_maps_folder = output_folder / 'Output Maps'
    mod_maps_folder = output_folder / 'Mod Maps'

    zip_name = 'Dynamic_Battle_Team_Map_Pack.zip'
    input_scenario_prefix = 'EDIT_'
    output_scenario_prefix = 'OUTPUT_'
    mod_scenario_prefix = 'DBT_'
    scenario_extension = '.aoe2scenario'
    armageddon = 'ARMAGEDDON_3V3'
    niebla = 'FOG_2V2'
    caves = 'CAVES_4V4'
    bosque_encantado = 'ENCHANTED_FOREST_2V2'
    catastrophic = 'CATASTROPHIC_4V4'
    earthquake = 'EARTHQUAKE_4V4'
    tsunami = 'TSUNAMI_3V3'
    vulkan = 'VULKAN_4V4'
    west_train = 'WILD_WEST_TRAIN_3V3'

    armageddon_class = ArmageddonMultiplayer(
        input_scenario_name=f'{input_scenario_prefix}{armageddon}',
        output_scenario_name=f'{output_scenario_prefix}{armageddon}'
    )

    fog_class = FogMultiplayer(
        input_scenario_name=f'{input_scenario_prefix}{niebla}',
        output_scenario_name=f'{output_scenario_prefix}{niebla}'
    )

    caves_class = CavesMultiplayer(
        input_scenario_name=f'{input_scenario_prefix}{caves}',
        output_scenario_name=f'{output_scenario_prefix}{caves}'
    )

    enchanted_forest_class = EnchantedForestMultiplayer(
        input_scenario_name=f'{input_scenario_prefix}{bosque_encantado}',
        output_scenario_name=f'{output_scenario_prefix}{bosque_encantado}'
    )
    catastrophic_class = CatastrophicMultiplayer(
        input_scenario_name=f'{input_scenario_prefix}{catastrophic}',
        output_scenario_name=f'{output_scenario_prefix}{catastrophic}'
    )

    earthquake_class = EarthquakeMultiplayer(
        input_scenario_name=f'{input_scenario_prefix}{earthquake}',
        output_scenario_name=f'{output_scenario_prefix}{earthquake}'
    )

    tsunami_class = TsunamiMultiplayer(
        input_scenario_name=f'{input_scenario_prefix}{tsunami}',
        output_scenario_name=f'{output_scenario_prefix}{tsunami}'
    )

    vulkan_class = VulkanMultiplayer(
        input_scenario_name=f'{input_scenario_prefix}{vulkan}',
        output_scenario_name=f'{output_scenario_prefix}{vulkan}'
    )

    west_train_class = WestTrainMultiplayer(
        input_scenario_name=f'{input_scenario_prefix}{west_train}',
        output_scenario_name=f'{output_scenario_prefix}{west_train}'
    )

    armageddon_class.convert()
    fog_class.convert()
    caves_class.convert()
    enchanted_forest_class.convert()
    catastrophic_class.convert()
    earthquake_class.convert()
    tsunami_class.convert()
    vulkan_class.convert()
    west_train_class.convert()

    shutil.copy(scenario_folder / f'{input_scenario_prefix}{armageddon}{scenario_extension}', edit_maps_folder)
    shutil.copy(scenario_folder / f'{input_scenario_prefix}{niebla}{scenario_extension}', edit_maps_folder)
    shutil.copy(scenario_folder / f'{input_scenario_prefix}{bosque_encantado}{scenario_extension}', edit_maps_folder)
    shutil.copy(scenario_folder / f'{input_scenario_prefix}{caves}{scenario_extension}', edit_maps_folder)
    shutil.copy(scenario_folder / f'{input_scenario_prefix}{catastrophic}{scenario_extension}', edit_maps_folder)
    shutil.copy(scenario_folder / f'{input_scenario_prefix}{earthquake}{scenario_extension}', edit_maps_folder)
    shutil.copy(scenario_folder / f'{input_scenario_prefix}{tsunami}{scenario_extension}', edit_maps_folder)
    shutil.copy(scenario_folder / f'{input_scenario_prefix}{vulkan}{scenario_extension}', edit_maps_folder)
    shutil.copy(scenario_folder / f'{input_scenario_prefix}{west_train}{scenario_extension}', edit_maps_folder)

    shutil.copy(scenario_folder / f'{output_scenario_prefix}{armageddon}{scenario_extension}', output_maps_folder)
    shutil.copy(scenario_folder / f'{output_scenario_prefix}{niebla}{scenario_extension}', output_maps_folder)
    shutil.copy(scenario_folder / f'{output_scenario_prefix}{bosque_encantado}{scenario_extension}', output_maps_folder)
    shutil.copy(scenario_folder / f'{output_scenario_prefix}{caves}{scenario_extension}', output_maps_folder)
    shutil.copy(scenario_folder / f'{output_scenario_prefix}{catastrophic}{scenario_extension}', output_maps_folder)
    shutil.copy(scenario_folder / f'{output_scenario_prefix}{earthquake}{scenario_extension}', output_maps_folder)
    shutil.copy(scenario_folder / f'{output_scenario_prefix}{tsunami}{scenario_extension}', output_maps_folder)
    shutil.copy(scenario_folder / f'{output_scenario_prefix}{vulkan}{scenario_extension}', output_maps_folder)
    shutil.copy(scenario_folder / f'{output_scenario_prefix}{west_train}{scenario_extension}', output_maps_folder)

    shutil.copy(scenario_folder / f'{output_scenario_prefix}{armageddon}{scenario_extension}', mod_maps_folder / f'{mod_scenario_prefix}{armageddon}{scenario_extension}')
    shutil.copy(scenario_folder / f'{output_scenario_prefix}{niebla}{scenario_extension}', mod_maps_folder / f'{mod_scenario_prefix}{niebla}{scenario_extension}')
    shutil.copy(scenario_folder / f'{output_scenario_prefix}{bosque_encantado}{scenario_extension}', mod_maps_folder / f'{mod_scenario_prefix}{bosque_encantado}{scenario_extension}')
    shutil.copy(scenario_folder / f'{output_scenario_prefix}{caves}{scenario_extension}', mod_maps_folder / f'{mod_scenario_prefix}{caves}{scenario_extension}')
    shutil.copy(scenario_folder / f'{output_scenario_prefix}{catastrophic}{scenario_extension}', mod_maps_folder / f'{mod_scenario_prefix}{catastrophic}{scenario_extension}')
    shutil.copy(scenario_folder / f'{output_scenario_prefix}{earthquake}{scenario_extension}', mod_maps_folder / f'{mod_scenario_prefix}{earthquake}{scenario_extension}')
    shutil.copy(scenario_folder / f'{output_scenario_prefix}{tsunami}{scenario_extension}', mod_maps_folder / f'{mod_scenario_prefix}{tsunami}{scenario_extension}')
    shutil.copy(scenario_folder / f'{output_scenario_prefix}{vulkan}{scenario_extension}', mod_maps_folder / f'{mod_scenario_prefix}{vulkan}{scenario_extension}')
    shutil.copy(scenario_folder / f'{output_scenario_prefix}{west_train}{scenario_extension}', mod_maps_folder / f'{mod_scenario_prefix}{west_train}{scenario_extension}')

    utils.zip_folder(output_folder, zip_name)
