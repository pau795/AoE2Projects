import os

from AoE2ScenarioParser.datasets.other import OtherInfo
from AoE2ScenarioParser.datasets.players import PlayerId
from AoE2ScenarioParser.datasets.terrains import TerrainId
from AoE2ScenarioParser.objects.data_objects.trigger import Trigger
from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario

from scenarios.lib import utils
from scenarios.lib.parser_project import ParserProject


class Template(ParserProject):

    def __init__(self, input_scenario_name: str, output_scenario_name: str):
        super().__init__(input_scenario_name, output_scenario_name)
        self.trigger_manager = self.scenario.trigger_manager
        self.map_manager = self.scenario.map_manager
        self.unit_manager = self.scenario.unit_manager
        self.xs_manager = self.scenario.xs_manager
        self.terrain_order = [TerrainId.WATER_AZURE, TerrainId.WATER_GREEN, TerrainId.WATER_YELLOW_DEEP]

    def process(self):
        terrain_atlas = utils.get_terrain_dict()
        terrain_list = []
        for tile in self.scenario.new.area().select_entire_map().to_coords(as_terrain=True):
            if tile.terrain_id not in terrain_list:
                terrain_list.append(tile.terrain_id)
        terrain_list.sort()
        for terrain in terrain_list:
            terrain_info = terrain_atlas[terrain]
            print(terrain, terrain_info['name'], terrain_info['is_water'])


if __name__ == '__main__':
    template_class = Template(
        input_scenario_name=f'EDIT_THREE_GORGES',
        output_scenario_name=f'EDIT_THREE_GORGES_TEST'
    )
    template_class.process()
