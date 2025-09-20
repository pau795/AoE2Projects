from genieutils.datfile import DatFile
from genieutils.graphic import GraphicDelta


class PlagueDat:
    def __init__(self, dat_file: DatFile):
        self.dat_file = dat_file
        self.set_smoke(9411, "green_glow")
        self.set_butterflies(9410, 12269, 9411, "butterflies_attack_x1")

    def set_smoke(self, graphic_id: int, smoke_particle: str):
        graphic = self.dat_file.graphics[graphic_id]
        graphic.particle_effect_name = smoke_particle
        graphic.layer = 10
        graphic.transparency = 0
        graphic.replay_delay = 0
        graphic.frame_count = 1
        graphic.frame_duration = 0
        graphic.sequence_type = 1
        graphic.mirroring_mode = 0
        graphic.angle_count = 1

    def set_butterflies(self, graphic_id: int, butterflies_graphic: int, smoke_graphic: int, sprite_name: str):
        graphic = self.dat_file.graphics[graphic_id]
        graphic.file_name = sprite_name
        graphic.layer = 20
        graphic.transparency = 0
        graphic.replay_delay = 0
        graphic.frame_count = 1
        graphic.frame_duration = 1
        graphic.sequence_type = 0
        graphic.mirroring_mode = 6
        graphic.angle_count = 1
        void_delta = GraphicDelta(graphic_id=-1, offset_x=0, offset_y=0, padding_1=0, padding_2=0, sprite_ptr=0, display_angle=-1)
        butterflies_delta = GraphicDelta(graphic_id=butterflies_graphic, offset_x=0, offset_y=0, padding_1=0, padding_2=0, sprite_ptr=0, display_angle=-1)
        glow_delta = GraphicDelta(graphic_id=smoke_graphic, offset_x=0, offset_y=0, padding_1=0, padding_2=0, sprite_ptr=0, display_angle=-1)
        graphic.deltas = [void_delta, butterflies_delta, glow_delta]
