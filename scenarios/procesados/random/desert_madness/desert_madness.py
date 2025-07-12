
from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario

from general.area_effects import AreaEffects
from general.barrel_petards import BarrelPetards
from general.bridges import Bridges
from gathering_areas.foraging_area import ForagingArea
from general.horses import Horses
from general.initial_attributes import InitialAttributes
from general.longbows import Longbows
from general.map_revealer import MapRevealer
from general.steppe_lancers import SteppeLancers
from respawn.shop_names import ShopNames

from respawn.respawn_attack_grounds import RespawnAttackGround
from gathering_areas.fishing_area import FishingArea
from gathering_areas.lubjerjack_area import LumberjackArea
from gathering_areas.stone_area import StoneArea
from gathering_areas.hunting_area import HuntingArea
from general.teleports import Teleports
import os



from AoE2ScenarioParser.datasets.players import PlayerId

from scenarios.lib.nomad_start import NomadStart
from scenarios.lib.parser_project import ParserProject


class DesertMadness(ParserProject):

    def __init__(self, input_scenario_name: str, output_scenario_name: str):
        super().__init__(input_scenario_name, output_scenario_name)        

    def process(self):
        try:
            trigger_data = self.scenario.actions.load_data_triggers()
            MapRevealer(self.scenario)
            Horses(self.scenario, trigger_data)
            AreaEffects(self.scenario, trigger_data)
            Bridges(self.scenario, trigger_data)
            SteppeLancers(self.scenario, trigger_data)
            Longbows(self.scenario, trigger_data)
            InitialAttributes(self.scenario)
            ShopNames(self.scenario, trigger_data)
            RespawnAttackGround(self.scenario, trigger_data)
            Teleports(self.scenario, trigger_data)
            FishingArea(self.scenario, trigger_data)
            LumberjackArea(self.scenario, trigger_data)
            StoneArea(self.scenario, trigger_data)
            HuntingArea(self.scenario, trigger_data)
            ForagingArea(self.scenario, trigger_data)
            BarrelPetards(self.scenario, trigger_data)
        except Exception as e:
            raise e


desert_madness = DesertMadness(
    input_scenario_name='desert_madness_parser',
    output_scenario_name='desert_madness_output',
)
desert_madness.convert()

