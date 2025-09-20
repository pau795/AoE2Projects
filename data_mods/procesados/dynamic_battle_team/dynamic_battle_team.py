from genieutils.datfile import DatFile
from genieutils.graphic import GraphicDelta
from multimedia_generator import constants


class DynamicBattleTeam:
    def __init__(self, dat_file: DatFile):
        self.dat_file = dat_file

    def hussite_smoke_graphic(self, graphic_id: int, smoke_graphic_id: int, sprite_name: str, graphic_name: str,):
        graphic = self.dat_file.graphics[graphic_id]
        graphic.name = graphic_name
        graphic.file_name = sprite_name
        graphic.layer = 20
        graphic.transparency = 1
        graphic.replay_delay = 0
        graphic.frame_count = 30
        graphic.frame_duration = 0.03666666895151138
        graphic.sequence_type = 3
        graphic.mirroring_mode = 6
        graphic.angle_count = 16
        graphic.speed_multiplier = 1
        void_delta = GraphicDelta(graphic_id=-1, offset_x=0, offset_y=0, padding_1=0, padding_2=0, sprite_ptr=0, display_angle=-1)
        shadow_delta = GraphicDelta(graphic_id=smoke_graphic_id, offset_x=0, offset_y=-100, padding_1=0, padding_2=0, sprite_ptr=0, display_angle=-1)
        graphic.deltas = [void_delta, shadow_delta]


if __name__ == "__main__":
    dat = DatFile.parse(constants.AOE_DAT_FILE_PATH)
    dynamic_battle_team = DynamicBattleTeam(dat)
    dynamic_battle_team.hussite_smoke_graphic(9500, 5314, "u_sie_hussite_wagon_walkA_x1", "HussiteWagonSmoke (Walk)")
    dat.save("output/empires2_x2_p1.dat")
