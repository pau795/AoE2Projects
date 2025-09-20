from pathlib import Path
from data_mods.lib.dat_project import DatProject
from data_mods.procesados.dynamic_battle_lan.alcatraz import AlcatrazDat
from data_mods.procesados.dynamic_battle_lan.plague import PlagueDat
from data_mods.procesados.dynamic_battle_lan.three_gorges import ThreeGorgesDat


class DynamicBattleLan(DatProject):

    def __init__(self, output_file: Path):
        super().__init__(output_file)

    def process(self):
        AlcatrazDat(self.dat_file)
        PlagueDat(self.dat_file)
        ThreeGorgesDat(self.dat_file)


if __name__ == "__main__":
    dat_mod_path = "C:\\Users\\pau_7\\Games\\Age of Empires 2 DE\\76561198074945033\\mods\\local\\Dynamic Battle LAN LOCAL\\resources\\_common\\dat"
    dynamic_battle_lan = DynamicBattleLan(Path(dat_mod_path))
    dynamic_battle_lan.convert()
