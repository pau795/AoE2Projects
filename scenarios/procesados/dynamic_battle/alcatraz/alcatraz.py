from AoE2ScenarioParser.datasets.terrains import TerrainId
from AoE2ScenarioParser.objects.support.area import Area

from scenarios.lib.parser_project import ParserProject
from scenarios.lib.unit_modifier import UnitModifier


class Alcatraz(ParserProject):

    def __init__(self, input_scenario_name: str, output_scenario_name: str):
        super().__init__(input_scenario_name, output_scenario_name)
        self.trigger_manager = self.scenario.trigger_manager
        self.data_triggers = self.scenario.actions.load_data_triggers()
        self.map_manager = self.scenario.map_manager
        self.unit_manager = self.scenario.unit_manager
        self.xs_manager = self.scenario.xs_manager

    # def bridge_stats(self):
    #     UnitModifier(self.scenario, UnitInfo.BRIDGE.ID, PlayerId.GAIA).create_triggers()

    def process_bridges(self):
        for key, area_list in self.data_triggers.areas.items():
            if "bridge" in key:
                area: Area = area_list[0]
                top_area: Area = self.scenario.new.area()
                bottom_area: Area = self.scenario.new.area()
                if area.get_width() > area.get_height():
                    top_area.x1 = area.x1
                    top_area.x2 = area.x1
                    top_area.y1 = area.y1 - 1
                    top_area.y2 = area.y2 + 1

                    bottom_area.x1 = area.x2
                    bottom_area.x2 = area.x2
                    bottom_area.y1 = area.y1 - 1
                    bottom_area.y2 = area.y2 + 1
                else:
                    top_area.x1 = area.x1 - 1
                    top_area.x2 = area.x2 + 1
                    top_area.y1 = area.y1
                    top_area.y2 = area.y1

                    bottom_area.x1 = area.x1 - 1
                    bottom_area.x2 = area.x2 + 1
                    bottom_area.y1 = area.y2
                    bottom_area.y2 = area.y2

                for tile1, tile2 in zip(top_area.to_coords(as_terrain=True), bottom_area.to_coords(as_terrain=True)):
                    print(f'{tile1.x}, {tile1.y}, {tile2.x}, {tile2.y}')
                    tile1.terrain_id = TerrainId.SHALLOWS
                    tile2.terrain_id = TerrainId.SHALLOWS

    def process(self):
        self.process_bridges()


if __name__ == '__main__':
    alcatraz_class = Alcatraz(
        input_scenario_name=f'alcatraz_editar',
        output_scenario_name=f'alcatraz_output'
    )
    alcatraz_class.convert()
