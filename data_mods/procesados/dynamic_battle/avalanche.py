from genieutils.datfile import DatFile
from genieutils.graphic import GraphicDelta
from genieutils.sound import SoundItem
from genieutils.terrainrestriction import TerrainRestriction

from multimedia_generator import constants


class Avalanche:
    def __init__(self, dat_file: DatFile):
        self.dat_file = dat_file
        self.set_rock_graphic(10639, "med_snowball_roll_1_x1", 10643)
        self.set_rock_graphic(10640, "med_snowball_roll_2_x1", 10643)
        self.set_rock_graphic(10641, "med_snowball_roll_3_x1", 10643)
        self.set_rock_graphic(10642, "lg_snowball_roll_1_x1", 10643)
        self.set_dust(10643, "dust_loop")
        self.set_avalanche_sound_graphic(10644, 642)
        self.snow_terrain_restriction(self.dat_file.terrain_restrictions[41])
        self.set_avalanche_sound(642)
        self.set_snowball_sound(643)

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

    def set_avalanche_sound_graphic(self, graphic_id: int, sound_id: int):
        graphic = self.dat_file.graphics[graphic_id]
        graphic.sound_id = 642

    def set_rock_graphic(self, graphic_id: int, sprite_name: str, dust_graphic_id: int, sound_id: int | None = None):
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
        if sound_id is not None:
            graphic.sound_id = sound_id
        void_delta = GraphicDelta(graphic_id=-1, offset_x=0, offset_y=0, padding_1=0, padding_2=0, sprite_ptr=0, display_angle=-1)
        dust_delta = GraphicDelta(graphic_id=dust_graphic_id, offset_x=0, offset_y=0, padding_1=0, padding_2=0, sprite_ptr=0, display_angle=-1)
        graphic.deltas = [void_delta, dust_delta]

    @staticmethod
    def snow_terrain_restriction(new_terrain_restriction: TerrainRestriction):
        for i, (_, _) in enumerate(zip(new_terrain_restriction.passable_buildable_dmg_multiplier, new_terrain_restriction.terrain_pass_graphics)):
            new_terrain_restriction.passable_buildable_dmg_multiplier[i] = 1
            new_terrain_restriction.terrain_pass_graphics[i].exit_tile_sprite_id = -1
            new_terrain_restriction.terrain_pass_graphics[i].enter_tile_sprite_id = 3586
            new_terrain_restriction.terrain_pass_graphics[i].walk_tile_sprite_id = 5707
            new_terrain_restriction.terrain_pass_graphics[i].walk_sprite_rate = 4

    def set_avalanche_sound(self, sound_id: int):
        sounds = [("avalanche_1", 33), ("avalanche_2", 33), ("avalanche_3", 34)]
        sound = self.dat_file.sounds[sound_id]
        sound.play_delay = 0
        sound.cache_time = 300000
        sound.total_probability = 100
        sound.items = [SoundItem(
            filename=filename,
            resource_id=-1,
            probability=probability,
            civilization=-1,
            icon_set=-1,
        ) for filename, probability in sounds]

    def set_snowball_sound(self, sound_id: int):
        sounds = [("snowball_roll_1", 33), ("snowball_roll_2", 33), ("snowball_roll_3", 34)]
        sound = self.dat_file.sounds[sound_id]
        sound.play_delay = 0
        sound.cache_time = 300000
        sound.total_probability = 100
        sound.items = [SoundItem(
            filename=filename,
            resource_id=-1,
            probability=probability,
            civilization=-1,
            icon_set=-1,
        ) for filename, probability in sounds]
