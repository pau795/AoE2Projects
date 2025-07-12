import math
import random
from AoE2ScenarioParser.datasets.other import OtherInfo
from AoE2ScenarioParser.datasets.players import PlayerId
from scenarios.lib.parser_project import ParserProject


class Deshielo(ParserProject):

    def __init__(self, input_scenario_name: str, output_scenario_name: str):
        super().__init__(input_scenario_name, output_scenario_name)
        self.map_manager = self.scenario.map_manager
        self.unit_manager = self.scenario.unit_manager

    def process(self):
        self.freeze()

    def freeze(self):
        x = 0.0
        while x < float(self.map_manager.map_width):
            y = 0.0
            while y < float(self.map_manager.map_height):
                self.unit_manager.add_unit(
                    player=PlayerId.GAIA,
                    unit_const=OtherInfo.ICE_NAVIGABLE.ID,
                    rotation=random.random() * 2 * math.pi,
                    x=x,
                    y=y,
                    z=0
                )
                y += 0.75
            x += 0.75


deshielo = Deshielo(
    input_scenario_name='el_deshielo',
    output_scenario_name='el_deshielo_output'
)
deshielo.convert()
