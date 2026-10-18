from genieutils.datfile import DatFile


class ThunderDunesDat(DatFile):
    def __init__(self, dat_file: DatFile):
        self.dat_file = dat_file
        self.set_lightning(10636, "lightning2")
        self.set_static_electricity(10637, "static_electricity")
        self.set_fast_smoke(10638, "smoke_medium_fast")
        self.set_rain(10643, "rain")
        self.set_cloud(10645, "storm_cloud")

    def set_lightning(self, graphic_id: int, lightning_particle: str):
        graphic = self.dat_file.graphics[graphic_id]
        graphic.particle_effect_name = lightning_particle
        graphic.layer = 30
        graphic.transparent_selection = 2
        graphic.replay_delay = 0
        graphic.frame_count = 1
        graphic.frame_duration = 1.1
        graphic.sequence_type = 9
        graphic.mirroring_mode = 0
        graphic.angle_count = 1

    def set_cloud(self, graphic_id: int, cloud_particle: str):
        graphic = self.dat_file.graphics[graphic_id]
        graphic.particle_effect_name = cloud_particle
        graphic.layer = 30
        graphic.transparent_selection = 1
        graphic.replay_delay = 0
        graphic.frame_count = 1
        graphic.frame_duration = 2.1333333333
        graphic.sequence_type = 0
        graphic.mirroring_mode = 0
        graphic.angle_count = 1

    def set_static_electricity(self, graphic_id: int, static_electricity_particle: str):
        graphic = self.dat_file.graphics[graphic_id]
        graphic.particle_effect_name = static_electricity_particle
        graphic.layer = 20
        graphic.transparent_selection = 1
        graphic.replay_delay = 0
        graphic.frame_count = 1
        graphic.frame_duration = 1
        graphic.sequence_type = 7
        graphic.mirroring_mode = 0
        graphic.angle_count = 1

    def set_fast_smoke(self, graphic_id: int, smoke_particle: str):
        graphic = self.dat_file.graphics[graphic_id]
        graphic.particle_effect_name = smoke_particle
        graphic.layer = 30
        graphic.transparent_selection = 1
        graphic.replay_delay = 0
        graphic.frame_count = 1
        graphic.frame_duration = 3.3
        graphic.sequence_type = 9
        graphic.mirroring_mode = 0
        graphic.angle_count = 1

    def set_rain(self, graphic_id: int, rain_particle: str):
        graphic = self.dat_file.graphics[graphic_id]
        graphic.particle_effect_name = rain_particle
        graphic.layer = 30
        graphic.transparent_selection = 1
        graphic.replay_delay = 0
        graphic.frame_count = 1
        graphic.frame_duration = 1.0666666667
        graphic.sequence_type = 1
        graphic.mirroring_mode = 0
        graphic.angle_count = 1

