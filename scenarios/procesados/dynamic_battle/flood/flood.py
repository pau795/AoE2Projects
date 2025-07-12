from scenarios.lib.flood_factory import FloodFactory
from scenarios.lib.parser_project import ParserProject


class Flood(ParserProject):

    def __init__(self, input_scenario_name: str, output_scenario_name: str):
        super().__init__(input_scenario_name, output_scenario_name)
        self.trigger_manager = self.scenario.trigger_manager
        self.trigger_data = self.scenario.actions.load_data_triggers()

    def process(self):
        init_flood_tile = self.trigger_data.tiles['flood_init'][0]
        init_terrain_tile = self.scenario.map_manager.get_tile(init_flood_tile.x, init_flood_tile.y)
        flood_limit_area = self.trigger_data.areas['flood_limit'][0]
        flood_factory = FloodFactory(self.scenario)
        flood_factory.bridge_stats()
        flood_factory.generate_flood(init_terrain_tile, flood_limit_area, self.trigger_data.tiles['waterfall'])


if __name__ == '__main__':
    flood = Flood(
        input_scenario_name=f'flood',
        output_scenario_name=f'flood_output'
    )
    flood.convert()

