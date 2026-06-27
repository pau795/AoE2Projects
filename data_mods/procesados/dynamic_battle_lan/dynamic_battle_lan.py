from pathlib import Path
from data_mods.lib.dat_project import DatProject
from data_mods.procesados.dynamic_battle_lan.alcatraz import AlcatrazDat
from data_mods.procesados.dynamic_battle_lan.plague import PlagueDat
from data_mods.procesados.dynamic_battle_lan.three_gorges import ThreeGorgesDat
from data_mods.procesados.dynamic_battle_lan.thunder_dunes import ThunderDunesDat
from data_mods.procesados.dynamic_battle_lan.west_train import WestTrain


class DynamicBattleLan(DatProject):
    # List of customized graphics used in this data mod:
    #   - 10630: Horizontal Sea Wall (Alcatraz)
    #   - 10631: Vertical Sea Wall (Alcatraz)
    #   - 10632: Butterflies Attack (Plague)
    #   - 10633: Green Glow (Plague)
    #   - 10634: Water Ripple (Three Gorges)
    #   - 10635: Hussite + Smoke (West Train)
    #   - 10636: Lightning (Thunder Dunes)
    #   - 10637: Static Electricity (Thunder Dunes)
    #   - 10638: Smoke Medium Fast (Thunder Dunes)

    def __init__(self, output_file: Path):
        super().__init__(output_file)

    def process(self):
        AlcatrazDat(self.dat_file)
        PlagueDat(self.dat_file)
        ThreeGorgesDat(self.dat_file)
        WestTrain(self.dat_file)
        ThunderDunesDat(self.dat_file)


if __name__ == "__main__":
    dat_mod_path = "C:\\Users\\pau_7\\Games\\Age of Empires 2 DE\\76561198074945033\\mods\\local\\Dynamic Battle LAN LOCAL\\resources\\_common\\dat"
    # dat_mod_path = 'output'
    dynamic_battle_lan = DynamicBattleLan(Path(dat_mod_path))
    dynamic_battle_lan.convert()
