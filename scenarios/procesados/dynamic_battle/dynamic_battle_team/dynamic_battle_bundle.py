import os
import shutil
import tempfile
import zipfile
from pathlib import Path

from leonroma.procesados.dynamic_battle.dynamic_battle_team.armaggeddon import Armageddon
from leonroma.procesados.dynamic_battle.dynamic_battle_team.bosque_encantado_multiplayer import BosqueEncantadoMultiplayer
from leonroma.procesados.dynamic_battle.dynamic_battle_team.castastrophic import Catastrophic
from leonroma.procesados.dynamic_battle.dynamic_battle_team.caves import Caves
from leonroma.procesados.dynamic_battle.dynamic_battle_team.earthquake_multiplayer import EarthquakeMultiplayer
from leonroma.procesados.dynamic_battle.dynamic_battle_team.niebla_multiplayer import NieblaMultiplayer
from leonroma.procesados.dynamic_battle.dynamic_battle_team.tsunami_multiplayer import TsunamiMultiplayer
from leonroma.procesados.dynamic_battle.dynamic_battle_team.vulkan_multiplayer import VulkanMultiplayer
from leonroma.procesados.dynamic_battle.dynamic_battle_team.west_train import WestTrain


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

    armageddon_class = Armageddon(
        steam_id=steam_id,
        input_scenario_name=f'{input_scenario_prefix}{armageddon}',
        output_scenario_name=f'{output_scenario_prefix}{armageddon}'
    )

    niebla_class = NieblaMultiplayer(
        input_scenario_name=f'{input_scenario_prefix}{niebla}',
        output_scenario_name=f'{output_scenario_prefix}{niebla}'
    )

    caves_class = Caves(
        input_scenario_name=f'{input_scenario_prefix}{caves}',
        output_scenario_name=f'{output_scenario_prefix}{caves}'
    )

    bosque_encantado_class = BosqueEncantadoMultiplayer(
        input_scenario_name=f'{input_scenario_prefix}{bosque_encantado}',
        output_scenario_name=f'{output_scenario_prefix}{bosque_encantado}'
    )
    catastrophic_class = Catastrophic(
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

    west_train_class = WestTrain(
        input_scenario_name=f'{input_scenario_prefix}{west_train}',
        output_scenario_name=f'{output_scenario_prefix}{west_train}'
    )

    armageddon_class.convert()
    niebla_class.convert()
    caves_class.convert()
    bosque_encantado_class.convert()
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

    zip_folder(output_folder, zip_name)


