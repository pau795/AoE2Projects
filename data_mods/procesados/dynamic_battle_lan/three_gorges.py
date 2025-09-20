from AoE2ScenarioParser.datasets.terrains import TerrainId
from AoE2ScenarioParser.datasets.trigger_lists import TerrainRestrictions
from genieutils.datfile import DatFile
from genieutils.terrainrestriction import TerrainRestriction

from scenarios.lib import utils


class ThreeGorgesDat:
    def __init__(self, dat_file: DatFile):
        self.dat_file = dat_file
        self.terrain_atlas = utils.get_terrain_dict()
        self.moddable_terrain = TerrainId.MODDABLE_NORMAL_WATER_1

        tr_land = self.dat_file.terrain_restrictions[7]
        tr_land_beach = self.dat_file.terrain_restrictions[10]
        tr_land_no_beach = self.dat_file.terrain_restrictions[40]
        tr_land.passable_buildable_dmg_multiplier[self.moddable_terrain] = 1
        tr_land_beach.passable_buildable_dmg_multiplier[self.moddable_terrain] = 1
        self.no_beach_terrain_restriction(tr_land_no_beach)

        mod_land = self.dat_file.terrain_block.terrains[self.moddable_terrain]
        mod_land.name_1 = "Floodable Land"
        mod_land.name_2 = "g_ds2"
        mod_land.is_water = 0
        mod_land.hide_in_editor = 0
        mod_land.colors = (176, 107, 120)

    def no_beach_terrain_restriction(self, new_terrain_restriction: TerrainRestriction):
        for i, (_, _) in enumerate(zip(new_terrain_restriction.passable_buildable_dmg_multiplier, new_terrain_restriction.terrain_pass_graphics)):
            new_terrain_restriction.passable_buildable_dmg_multiplier[i] = 1 if self.terrain_atlas[i]['is_water'] == 32 else 0
            new_terrain_restriction.terrain_pass_graphics[i].exit_tile_sprite_id = -1
            new_terrain_restriction.terrain_pass_graphics[i].enter_tile_sprite_id = -1
            new_terrain_restriction.terrain_pass_graphics[i].walk_tile_sprite_id = -1
            new_terrain_restriction.terrain_pass_graphics[i].walk_sprite_rate = 0

