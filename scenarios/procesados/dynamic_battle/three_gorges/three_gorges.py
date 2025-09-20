from AoE2ScenarioParser.datasets.players import PlayerId
from AoE2ScenarioParser.datasets.terrains import TerrainId

from scenarios.lib.flood_factory import FloodFactory
from scenarios.lib.parser_project import ParserProject


class Template(ParserProject):

    def __init__(self, input_scenario_name: str, output_scenario_name: str):
        super().__init__(input_scenario_name, output_scenario_name)
        self.trigger_manager = self.scenario.trigger_manager
        self.map_manager = self.scenario.map_manager
        self.unit_manager = self.scenario.unit_manager
        self.xs_manager = self.scenario.xs_manager
        self.flood_layers = [TerrainId.WATER_AZURE, TerrainId.WATER_GREEN, TerrainId.WATER_YELLOW_DEEP]
        self.limit_terrains = [TerrainId.BEACH, TerrainId.BEACH_WHITE_VEGETATION, TerrainId.MODDABLE_NORMAL_WATER_1]
        self.data_triggers = self.scenario.actions.load_data_triggers()
        self.player_list = [PlayerId.ONE, PlayerId.TWO]

    def process(self):
        layers_scenario = self.load_scenario(f'{self.input_scenario_name}_LAYERS')
        for tile in layers_scenario.new.area().select_entire_map().to_coords(as_terrain=True):
            if tile.layer in self.flood_layers:
                self.map_manager.get_tile(tile.x, tile.y).layer = tile.layer
        self.xs_manager.add_script("three_gorges.xs")
        buildings_land_and_beach = self.trigger_manager.add_trigger("Set Buildings on Land and Beach")
        buildings_land_and_beach.new_effect.script_call(message="buildings_on_land_and_beach();")
        flood_factory = FloodFactory(self.scenario, self.player_list)
        waterfall_dict = {}
        for i, key in enumerate(["waterfall_r2l", "waterfall_l2r", "waterfall_d"]):
            if key in self.data_triggers.tiles:
                waterfall_dict[i] = self.data_triggers.tiles[key]
        initial_tiles = [self.map_manager.get_tile(tile.x, tile.y) for tile in self.data_triggers.tiles["init_flood"]]
        first_flood_trigger = flood_factory.generate_flood(initial_tiles, self.limit_terrains, False, layer_mask=[TerrainId.WATER_AZURE], kill=False)
        second_flood_trigger = flood_factory.generate_flood(initial_tiles, self.limit_terrains, False, layer_mask=[TerrainId.WATER_AZURE, TerrainId.WATER_GREEN], kill=False)
        third_flood_trigger = flood_factory.generate_flood(initial_tiles, self.limit_terrains, False, waterfall_dict, layer_mask=[TerrainId.WATER_AZURE, TerrainId.WATER_GREEN, TerrainId.WATER_YELLOW_DEEP], kill=True)

        first_flood_trigger.new_condition.timer(600)
        second_flood_trigger.new_condition.timer(900)
        third_flood_trigger.new_condition.timer(1200)
        third_flood_trigger.new_effect.script_call(message="buildings_on_land_no_beach();")
        final_flood_trigger = self.trigger_manager.add_trigger("Final Flood")
        final_flood_trigger.new_condition.timer(1260)
        final_flood_trigger.new_effect.script_call(message="units_land_no_beach();")

        beach_shores = self.trigger_manager.add_trigger("Beach Shores")
        beach_shores.new_condition.timer(2)
        for tile in self.scenario.new.area().select_entire_map().to_coords(as_terrain=True):
            if tile.terrain_id == TerrainId.BEACH:
                tile.terrain_id = TerrainId.MODDABLE_NORMAL_WATER_1
                beach_shores.new_effect.create_object(
                    source_player=PlayerId.GAIA,
                    object_list_unit_id=FloodFactory.BEACH_BRIDGE,
                    location_x=tile.x,
                    location_y=tile.y
                )
            if tile.layer in self.flood_layers:
                tile.layer = -1
        beach_shores.new_effect.kill_object(
            object_list_unit_id=FloodFactory.BEACH_BRIDGE,
            source_player=PlayerId.GAIA
        )


if __name__ == '__main__':
    template_class = Template(
        input_scenario_name=f'EDIT_THREE_GORGES',
        output_scenario_name=f'OUTPUT_THREE_GORGES'
    )
    template_class.convert()
