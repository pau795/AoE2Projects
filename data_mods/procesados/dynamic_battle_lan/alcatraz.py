from genieutils.datfile import DatFile
from genieutils.graphic import GraphicDelta
from multimedia_generator import constants


class AlcatrazDat:
    def __init__(self, dat_file: DatFile):
        self.dat_file = dat_file
        self.set_wall(9400, "horizontal_sea_wall_x1")
        self.set_wall(9401, "vertical_sea_wall_x1")

    def set_wall(self, graphic_id: int, sprite_name: str):
        graphic = self.dat_file.graphics[graphic_id]
        graphic.file_name = sprite_name
        graphic.layer = 19
        graphic.transparency = 1
        graphic.replay_delay = 0
        graphic.frame_count = 1
        graphic.frame_duration = 0
        graphic.sequence_type = 0
        graphic.mirroring_mode = 0
        graphic.angle_count = 1

    def set_directional_wall(self, graphic_id:int, sprite_name: str):
        graphic = self.dat_file.graphics[graphic_id]
        graphic.file_name = sprite_name
        graphic.layer = 20
        graphic.transparency = 1
        graphic.replay_delay = 0
        graphic.frame_count = 1
        graphic.frame_duration = 0
        graphic.sequence_type = 2
        graphic.mirroring_mode = 0
        graphic.angle_count = 4

