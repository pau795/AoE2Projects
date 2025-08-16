from AoE2ScenarioParser.datasets.other import OtherInfo
from AoE2ScenarioParser.datasets.players import PlayerId

from scenarios.lib.parser_project import ParserProject


class MapMarker(ParserProject):

    def __init__(self, input_scenario_name: str, output_scenario_name: str):
        super().__init__(input_scenario_name, output_scenario_name)
        horizontal_sections = 3
        vertical_sections = 10
        center = True
        self.horizontal_sections = horizontal_sections if horizontal_sections >= 1 else 1
        self.vertical_sections = vertical_sections if horizontal_sections >= 1 else 1
        self.center = center

    def process(self):
        unit_manager = self.scenario.unit_manager
        map_manager = self.scenario.map_manager
        horizontal_width = map_manager.map_width / self.horizontal_sections
        vertical_height = map_manager.map_height / self.vertical_sections
        if self.center:
            unit_manager.add_unit(
                player=PlayerId.GAIA,
                unit_const=OtherInfo.FLAG_B.ID,
                rotation=0,
                x=map_manager.map_width / 2.0,
                y=map_manager.map_height / 2.0,
                z=0
            )
        x = 0.0
        while x <= map_manager.map_width:
            y = 0.0
            while y <= map_manager.map_height:
                unit_manager.add_unit(
                    player=PlayerId.GAIA,
                    unit_const=OtherInfo.FLAG_A.ID,
                    rotation=0,
                    x=x,
                    y=y,
                    z=0
                )
                y += vertical_height
            x += horizontal_width


marker = MapMarker(
    input_scenario_name='test',
    output_scenario_name='test_output',

)
marker.convert()
