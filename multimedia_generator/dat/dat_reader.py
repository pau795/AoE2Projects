from genieutils.datfile import DatFile
from multimedia_generator import constants
from multimedia_generator.dat.dat_model import UnitData, GraphicData, GraphicDelta
from multimedia_generator.utils import Singleton


class DatReader(metaclass=Singleton):
    def __init__(self):
        self.dat = DatFile.parse(constants.AOE_DAT_FILE_PATH)

    def get_units(self, unit_list: list[int]) -> list[UnitData]:
        return [self.get_unit_data(unit_id) for unit_id in unit_list]

    def get_unit(self, unit_id: int) -> UnitData:
        return self.get_unit_data(unit_id)

    def get_graphic_data(self, graphic_id: int) -> GraphicData | None:
        if graphic_id == -1:
            return None
        graphic_object = self.dat.graphics[graphic_id]
        graphic_file = f'{graphic_object.file_name}.sld' if not constants.uhd_graphics else f'{graphic_object.file_name}.sld'.replace("x1", "x2")
        graphic_frames_per_angle = graphic_object.frame_count
        graphic_frame_duration = graphic_object.frame_duration
        graphic_mirror_mode = graphic_object.mirroring_mode
        graphic_deltas_object = graphic_object.deltas
        deltas = [GraphicDelta(delta.graphic_id, delta.offset_x, delta.offset_y) for delta in graphic_deltas_object]
        return GraphicData(graphic_id, graphic_file, graphic_frames_per_angle, graphic_frame_duration, graphic_mirror_mode, deltas)

    def get_unit_data(self, unit_id: int) -> UnitData:
        unit_data = self.dat.civs[constants.default_civ].units[unit_id]
        reload_time = unit_data.type_50.reload_time
        name_string_id = unit_data.language_dll_name
        standing_graphic_id = unit_data.standing_graphic[0]
        walking_graphic_id = unit_data.dead_fish.walking_graphic
        attack_graphic_id = unit_data.type_50.attack_graphic
        idle_attack_graphid_id = unit_data.creatable.idle_attack_graphic
        icon_id = unit_data.icon_id
        unit = UnitData(unit_id, name_string_id, icon_id, reload_time)
        if standing_graphic_id != -1:
            unit.standing_graphic = self.get_graphic_data(standing_graphic_id)
        if walking_graphic_id != -1:
            unit.walking_graphic = self.get_graphic_data(walking_graphic_id)
        if attack_graphic_id != -1:
            unit.attack_graphic = self.get_graphic_data(attack_graphic_id)
        if idle_attack_graphid_id != -1:
            unit.idle_attack_graphic = self.get_graphic_data(idle_attack_graphid_id)
        return unit
