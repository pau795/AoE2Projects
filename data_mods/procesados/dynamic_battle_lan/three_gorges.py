from AoE2ScenarioParser.datasets.terrains import TerrainId
from AoE2ScenarioParser.datasets.trigger_lists import TerrainRestrictions
from genieutils.datfile import DatFile
from genieutils.terrainrestriction import TerrainRestriction

from scenarios.lib import utils


class ThreeGorgesDat:
    def __init__(self, dat_file: DatFile):
        self.dat_file = dat_file
        self.terrain_atlas = utils.get_terrain_dict()

        self.set_water_ripple(9420, "flood_splash")

        self.new_shore_terrain = TerrainId.MODDABLE_SHALLOWS_1  # This terrain is used on the shores
        self.new_first_flood_terrain = TerrainId.MODDABLE_GRASS_1  # This terrain is used on the first flood, just visual
        self.new_second_flood_terrain = TerrainId.MODDABLE_GRASS_2  # This terrain is used on the second flood, just visual

        tr_land_beach = self.dat_file.terrain_restrictions[10]
        tr_land_no_beach = self.dat_file.terrain_restrictions[40]
        tr_land_beach.passable_buildable_dmg_multiplier[self.new_shore_terrain] = 1
        self.no_beach_terrain_restriction(tr_land_no_beach)

        mod_land = self.dat_file.terrain_block.terrains[self.new_shore_terrain]
        mod_land.name_1 = "Mixed Shore"
        mod_land.name_2 = "g_ds2"
        mod_land.is_water = 0
        mod_land.hide_in_editor = 0
        mod_land.colors = (137, 124, 88)

        mod_land = self.dat_file.terrain_block.terrains[self.new_first_flood_terrain]
        mod_land.name_1 = "First Flood"
        mod_land.name_2 = "g_wt_brown"
        mod_land.hide_in_editor = 0
        mod_land.colors = (50, 40, 30)

        mod_land = self.dat_file.terrain_block.terrains[self.new_second_flood_terrain]
        mod_land.name_1 = "Second Flood"
        mod_land.name_2 = "g_wt_yellow"
        mod_land.hide_in_editor = 0
        mod_land.colors = (50, 40, 30)

    def no_beach_terrain_restriction(self, new_terrain_restriction: TerrainRestriction):
        for i, (_, _) in enumerate(zip(new_terrain_restriction.passable_buildable_dmg_multiplier, new_terrain_restriction.terrain_pass_graphics)):
            new_terrain_restriction.passable_buildable_dmg_multiplier[i] = 1 if self.terrain_atlas[i]['is_water'] == 32 else 0
            new_terrain_restriction.terrain_pass_graphics[i].exit_tile_sprite_id = -1
            new_terrain_restriction.terrain_pass_graphics[i].enter_tile_sprite_id = -1
            new_terrain_restriction.terrain_pass_graphics[i].walk_tile_sprite_id = -1
            new_terrain_restriction.terrain_pass_graphics[i].walk_sprite_rate = 0

    def set_water_ripple(self, graphic_id: int, particle: str):
        graphic = self.dat_file.graphics[graphic_id]
        graphic.particle_effect_name = particle
        graphic.layer = 30
        graphic.transparency = 1
        graphic.replay_delay = 0
        graphic.frame_count = 1
        graphic.frame_duration = 3.33
        graphic.sequence_type = 1
        graphic.mirroring_mode = 0
        graphic.angle_count = 1
