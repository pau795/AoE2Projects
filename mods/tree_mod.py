import shutil
from pathlib import Path

from genieutils.datfile import DatFile

from multimedia_generator import constants
from tree_dict import tree_dict

base_path = Path('D:\\cosas\\Utilidades\\age\\mods\\flat trees')
sld_path = base_path / 'sld'
mod_path = base_path / 'mod'

for tree_object in tree_dict:
    graphic_name = tree_object["graphic"]
    tree_type = tree_object["type"]
    angle_count = tree_object["angle_count"]
    match tree_type:
        case "tree":
            shutil.copy(sld_path / f"tree_template_{angle_count}.png.sld", mod_path / graphic_name)
        case "felled":
            shutil.copy(sld_path / f"felled_tree_template_{angle_count}.png.sld", mod_path / graphic_name)
        case "stump":
            shutil.copy(sld_path / "stump_tree_template.png.sld", mod_path / graphic_name)


dat_file = DatFile.parse(constants.AOE_DAT_FILE_PATH)
set_angle_count = set()
i = 0
for tree_object in tree_dict:
    game_tree = dat_file.civs[0].units[tree_object["object_id"]]
    graphic_id = game_tree.standing_graphic[0]
    graphic_tree = dat_file.graphics[graphic_id]
    if graphic_tree.file_name in tree_object["graphic"]:
        angle_count = graphic_tree.angle_count
        set_angle_count.add(angle_count)
        i += 1
        print(angle_count)


print(f"{i=}, {len(tree_dict)}")
print(f"angle_count: {set_angle_count}")
