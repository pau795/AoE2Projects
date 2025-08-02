from genieutils.datfile import DatFile
from genieutils.graphic import GraphicDelta
from multimedia_generator import constants


class RockGraphics:
    def __init__(self, dat_file: DatFile):
        self.dat_file = dat_file

    def set_rock_graphic(self, graphic_id: int, sprite_name: str, shadow_graphic_id: int):
        graphic = self.dat_file.graphics[graphic_id]
        graphic.file_name = sprite_name
        graphic.layer = 30
        graphic.transparency = 0
        graphic.replay_delay = 0
        graphic.frame_count = 30
        graphic.frame_duration = 0.01549999974668026
        graphic.sequence_type = 1
        graphic.mirroring_mode = 0
        graphic.angle_count = 1
        void_delta = GraphicDelta(graphic_id=-1, offset_x=0, offset_y=0, padding_1=0, padding_2=0, sprite_ptr=0, display_angle=-1)
        shadow_delta = GraphicDelta(graphic_id=shadow_graphic_id, offset_x=0, offset_y=0, padding_1=0, padding_2=0, sprite_ptr=0, display_angle=-1)
        graphic.deltas = [void_delta, shadow_delta]

    def set_rock_shadow(self, graphic_id: int, sprite_name: str):
        graphic = self.dat_file.graphics[graphic_id]
        graphic.file_name = sprite_name
        graphic.layer = 10
        graphic.transparency = 0
        graphic.replay_delay = 0
        graphic.frame_count = 30
        graphic.duration = 0.01549999974668026
        graphic.sequence_type = 1
        graphic.mirroring_mode = 0
        graphic.angle_count = 1


if __name__ == "__main__":
    dat = DatFile.parse(constants.AOE_DAT_FILE_PATH)
    rock_graphics = RockGraphics(dat)
    rock_graphics.set_rock_shadow(9511, "p_rock_med_shadow_x1")
    rock_graphics.set_rock_shadow(9513, "p_rock_big_shadow_x1")

    rock_graphics.set_rock_graphic(9510, "p_rock_med_x1", 9511)
    rock_graphics.set_rock_graphic(9512, "p_rock_big_x1", 9513)
    dat.save("C:\\Users\\pau_7\\Games\\Age of Empires 2 DE\\76561198074945033\\mods\\local\\Esfinge\\resources\\_common\\dat\\empires2_x2_p1.dat")
