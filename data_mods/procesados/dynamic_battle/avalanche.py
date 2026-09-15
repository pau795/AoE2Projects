from genieutils.datfile import DatFile
from genieutils.graphic import GraphicDelta
from genieutils.terrainrestriction import TerrainRestriction


class Avalanche:
    def __init__(self, dat_file: DatFile):
        self.dat_file = dat_file
        self.set_snowball_graphic(10639, "med_snowball_roll_1_x1", 10642)
        self.set_snowball_graphic(10640, "med_snowball_roll_2_x1", 10642)
        self.set_snowball_graphic(10641, "lg_snowball_roll_1_x1", 10642)
        self.set_dust(10642, "dust_loop")
        self.set_snow_rock_graphic(10643, "rock_snow_x1")
        self.snow_terrain_restriction(self.dat_file.terrain_restrictions[41])

    def set_dust(self, graphic_id: int, particle_name: str):
        graphic = self.dat_file.graphics[graphic_id]
        graphic.particle_effect_name = particle_name
        graphic.layer = 10
        graphic.transparent_selection = 1
        graphic.replay_delay = 0
        graphic.frame_count = 1
        graphic.frame_duration = 0
        graphic.sequence_type = 1
        graphic.mirroring_mode = 0
        graphic.angle_count = 1

    def set_snowball_graphic(self, graphic_id: int, sprite_name: str, dust_graphic_id: int):
        graphic = self.dat_file.graphics[graphic_id]
        graphic.file_name = sprite_name
        graphic.layer = 20
        graphic.transparency = 0
        graphic.replay_delay = 0
        graphic.frame_count = 10
        graphic.frame_duration = 0.10
        graphic.sequence_type = 1
        graphic.mirroring_mode = 0
        graphic.angle_count = 1
        void_delta = GraphicDelta(graphic_id=-1, offset_x=0, offset_y=0, padding_1=0, padding_2=0, sprite_ptr=0, display_angle=-1)
        dust_delta = GraphicDelta(graphic_id=dust_graphic_id, offset_x=0, offset_y=0, padding_1=0, padding_2=0, sprite_ptr=0, display_angle=-1)
        graphic.deltas = [void_delta, dust_delta]

    def set_snow_rock_graphic(self, graphic_id: int, sprite_name: str,):
        graphic = self.dat_file.graphics[graphic_id]
        graphic.file_name = sprite_name
        graphic.layer = 20
        graphic.transparency = 1
        graphic.replay_delay = 0
        graphic.frame_count = 1
        graphic.frame_duration = 0
        graphic.sequence_type = 6
        graphic.mirroring_mode = 0
        graphic.angle_count = 6

    @staticmethod
    def snow_terrain_restriction(new_terrain_restriction: TerrainRestriction):
        for i, (_, _) in enumerate(zip(new_terrain_restriction.passable_buildable_dmg_multiplier, new_terrain_restriction.terrain_pass_graphics)):
            new_terrain_restriction.passable_buildable_dmg_multiplier[i] = 1
            new_terrain_restriction.terrain_pass_graphics[i].exit_tile_sprite_id = -1
            new_terrain_restriction.terrain_pass_graphics[i].enter_tile_sprite_id = 3586
            new_terrain_restriction.terrain_pass_graphics[i].walk_tile_sprite_id = 5707
            new_terrain_restriction.terrain_pass_graphics[i].walk_sprite_rate = 4


