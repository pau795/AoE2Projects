from copy import deepcopy
from pathlib import Path

from AoE2ScenarioParser.datasets.buildings import BuildingInfo
from genieutils.graphic import GraphicDelta, Graphic

from data_mods.lib.dat_project import DatProject
from data_mods.lib.id_constants import GraphicConstants


class ClashRoyaleDat(DatProject):
    GRAPHIC_BOAR_IDLE = 2455
    GRAPHIC_BOAR_WALKING = 3238
    GRAPHIC_BOAR_ATTACKING = 2453
    GRAPHIC_VILLAGER_IDLE = 1284
    GRAPHIC_VILLAGER_ATTACKING = 1278

    def __init__(self, output_file: Path):
        super().__init__(output_file)

    def process(self):
        self.hog_rider()

    def copy_graphic(self, target_graphic_id: int, source_graphic_id: int) -> Graphic:
        graphic = deepcopy(self.dat_file.graphics[source_graphic_id])
        graphic.id = target_graphic_id
        self.dat_file.graphics[target_graphic_id] = graphic
        return graphic

    def hog_rider(self):
        void_delta = GraphicDelta(graphic_id=-1, offset_x=0, offset_y=0, padding_1=0, padding_2=0, sprite_ptr=0, display_angle=-1)
        villager_idle_delta = GraphicDelta(graphic_id=self.GRAPHIC_VILLAGER_IDLE, offset_x=0, offset_y=-12, padding_1=0, padding_2=0, sprite_ptr=0, display_angle=-1)
        villager_attack_delta = GraphicDelta(graphic_id=self.GRAPHIC_VILLAGER_ATTACKING, offset_x=0, offset_y=-12, padding_1=0, padding_2=0, sprite_ptr=0, display_angle=-1)

        graphic = self.copy_graphic(GraphicConstants.HOG_RIDER_IDLE, self.GRAPHIC_BOAR_IDLE)
        graphic.layer = 21
        graphic.deltas = [void_delta, villager_idle_delta]

        graphic = self.copy_graphic(GraphicConstants.HOG_RIDER_WALKING, self.GRAPHIC_BOAR_WALKING)
        graphic.layer = 21
        graphic.deltas = [void_delta, villager_idle_delta]

        graphic = self.copy_graphic(GraphicConstants.HOG_RIDER_ATTACK, self.GRAPHIC_BOAR_ATTACKING)
        graphic.layer = 21
        for i, sound in enumerate(graphic.angle_sounds):
            sound.sound_id_2 = self.dat_file.graphics[self.GRAPHIC_VILLAGER_ATTACKING].angle_sounds[i].sound_id
            sound.sound_id_3 = self.dat_file.graphics[self.GRAPHIC_VILLAGER_ATTACKING].angle_sounds[i].sound_id_2
            sound.wwise_sound_id_2 = self.dat_file.graphics[self.GRAPHIC_VILLAGER_ATTACKING].angle_sounds[i].wwise_sound_id
            sound.wwise_sound_id_3 = self.dat_file.graphics[self.GRAPHIC_VILLAGER_ATTACKING].angle_sounds[i].wwise_sound_id_2
            sound.frame_num_2 = self.dat_file.graphics[self.GRAPHIC_VILLAGER_ATTACKING].angle_sounds[i].frame_num
            sound.frame_num_3 = self.dat_file.graphics[self.GRAPHIC_VILLAGER_ATTACKING].angle_sounds[i].frame_num_2

        graphic.angle_sounds = self.dat_file.graphics[self.GRAPHIC_VILLAGER_ATTACKING].angle_sounds
        graphic.deltas = [void_delta, villager_attack_delta]

    def bridges(self):
        bridge_list = [
            BuildingInfo.BRIDGE_A_MIDDLE.ID,
            BuildingInfo.BRIDGE_A_CRACKED.ID,
            BuildingInfo.BRIDGE_A_BROKEN_TOP.ID,
            BuildingInfo.BRIDGE_A_BROKEN_BOTTOM.ID,
            BuildingInfo.BRIDGE_B_TOP.ID,
            BuildingInfo.BRIDGE_B_BOTTOM.ID,
            BuildingInfo.BRIDGE_B_MIDDLE.ID,
            BuildingInfo.BRIDGE_B_MIDDLE.ID,
            BuildingInfo.BRIDGE_B_CRACKED.ID,
            BuildingInfo.BRIDGE_B_BROKEN_TOP.ID,
            BuildingInfo.BRIDGE_B_BROKEN_BOTTOM.ID,
            BuildingInfo.BRIDGE_C_TOP.ID,
            BuildingInfo.BRIDGE_C_BOTTOM.ID,
            BuildingInfo.BRIDGE_C_MIDDLE.ID,
            BuildingInfo.BRIDGE_C_CRACKED.ID,
            BuildingInfo.BRIDGE_C_BROKEN_TOP.ID,
            BuildingInfo.BRIDGE_C_BROKEN_BOTTOM.ID,
            BuildingInfo.BRIDGE_D_TOP.ID,
            BuildingInfo.BRIDGE_D_BOTTOM.ID,
            BuildingInfo.BRIDGE_D_MIDDLE.ID,
            BuildingInfo.BRIDGE_D_CRACKED.ID,
            BuildingInfo.BRIDGE_D_BROKEN_TOP.ID,
            BuildingInfo.BRIDGE_D_BROKEN_BOTTOM.ID,
            BuildingInfo.WOODEN_BRIDGE_A_TOP.ID,
            BuildingInfo.WOODEN_BRIDGE_A_BOTTOM.ID,
            BuildingInfo.WOODEN_BRIDGE_A_MIDDLE.ID,
            BuildingInfo.WOODEN_BRIDGE_B_TOP.ID,
            BuildingInfo.WOODEN_BRIDGE_B_BOTTOM.ID,
            BuildingInfo.WOODEN_BRIDGE_B_MIDDLE.ID,
        ]
        
        for civ in self.dat_file.civs[1:]:
            for bridge_id in bridge_list:
                unit = civ.units[bridge_id]
                unit.collision_size_x = 0.25
                unit.collision_size_y = 0.25
                unit.collision_size_z = 0
                unit.outline_size_x = 0.25
                unit.outline_size_y = 0.25
                unit.outline_size_z = 1
                unit.clearance_size = (0.25, 0.25)


if __name__ == "__main__":
    dat_mod_path = "C:\\Users\\pau_7\\Games\\Age of Empires 2 DE\\76561198074945033\\mods\\local\\Clash Royale-LOCAL\\resources\\_common\\dat"
    clash_royale_dat = ClashRoyaleDat(Path(dat_mod_path))
    clash_royale_dat.convert()
