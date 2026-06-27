from genieutils.datfile import DatFile
from genieutils.sound import SoundItem


class ThunderDunesDat(DatFile):
    def __init__(self, dat_file: DatFile):
        self.dat_file = dat_file
        self.set_lightning_sound(640)
        self.set_static_electricity_sound(641)
        self.set_lightning(10636, "lightning2", 640)
        self.set_static_electricity(10637, "static_electricity", 641)
        self.set_fast_smoke(10638, "smoke_medium_fast")

    def set_lightning(self, graphic_id: int, lightning_particle: str, sound_id: int):
        graphic = self.dat_file.graphics[graphic_id]
        graphic.particle_effect_name = lightning_particle
        graphic.layer = 30
        graphic.transparent_selection = 2
        graphic.replay_delay = 0
        graphic.frame_count = 1
        graphic.frame_duration = 1.1
        graphic.sequence_type = 9
        graphic.mirroring_mode = 0
        graphic.sound_id = sound_id
        graphic.angle_count = 1

    def set_static_electricity(self, graphic_id: int, static_electricity_particle: str, sound_id):
        graphic = self.dat_file.graphics[graphic_id]
        graphic.particle_effect_name = static_electricity_particle
        graphic.layer = 20
        graphic.transparent_selection = 1
        graphic.replay_delay = 0
        graphic.frame_count = 1
        graphic.frame_duration = 1
        graphic.sequence_type = 7
        graphic.mirroring_mode = 0
        graphic.editor_flag = 1
        graphic.sound_id = sound_id
        graphic.angle_count = 1

    def set_fast_smoke(self, graphic_id: int, lightning_particle: str):
        graphic = self.dat_file.graphics[graphic_id]
        graphic.particle_effect_name = lightning_particle
        graphic.layer = 30
        graphic.transparent_selection = 1
        graphic.replay_delay = 0
        graphic.frame_count = 1
        graphic.frame_duration = 3.3
        graphic.sequence_type = 9
        graphic.mirroring_mode = 0
        graphic.angle_count = 1

    def set_static_electricity_sound(self, sound_id: int):
        sounds = [("static_electricity_1", 33), ("static_electricity_2", 33), ("static_electricity_3", 34)]
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

    def set_lightning_sound(self, sound_id: int):
        sounds = [("lightning_bolt_1", 33), ("lightning_bolt_2", 33), ("lightning_bolt_3", 34)]
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


