import json

from genieutils.datfile import DatFile

from multimedia_generator import constants


# dat_file = DatFile.parse(constants.AOE_DAT_FILE_PATH)
dat_file = DatFile.parse("C:\\Users\\pau_7\\Games\\Age of Empires 2 DE\\76561198074945033\\mods\\local\\Dynamic Battle LAN LOCAL\\resources\\_common\\dat\\empires2_x2_p1.dat")
restriction = dat_file.terrain_restrictions[40]
for j, (dmg, terrain_graphic) in enumerate(zip(restriction.passable_buildable_dmg_multiplier, restriction.terrain_pass_graphics)):
    if dmg != 0:
        terrain = dat_file.terrain_block.terrains[j]
        print(j, terrain.name, terrain.is_water, dmg)

# dict1 = {}
# for i, restriction in enumerate(dat_file.terrain_restrictions):
#     dict1[i] = restriction.passable_buildable_dmg_multiplier
#
# print(json.dumps(dict1))
