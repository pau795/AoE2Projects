import math
import random
from pathlib import Path

from AoE2ScenarioParser.datasets.buildings import BuildingInfo
from AoE2ScenarioParser.datasets.other import OtherInfo
from AoE2ScenarioParser.datasets.players import PlayerId
from AoE2ScenarioParser.datasets.terrains import TerrainId
from AoE2ScenarioParser.datasets.trigger_lists import ObjectAttribute, Operation, TimeUnit

from scenarios.lib.civ_settings import CivSettings
from scenarios.lib.flood_factory import FloodFactory
from scenarios.lib.parser_project import ParserProject


class ThreeGorges(ParserProject):
    RANDOM_SEED = 11111
    SMOKE_FLAG = OtherInfo.FLAG_I.ID

    def __init__(self, input_scenario_name: str, output_scenario_name: str):
        super().__init__(input_scenario_name, output_scenario_name)
        self.trigger_manager = self.scenario.trigger_manager
        self.map_manager = self.scenario.map_manager
        self.unit_manager = self.scenario.unit_manager
        self.xs_manager = self.scenario.xs_manager
        self.flood_layers = [TerrainId.WATER_AZURE, TerrainId.WATER_GREEN, TerrainId.WATER_YELLOW_DEEP]
        self.limit_terrains = [TerrainId.BEACH, TerrainId.BEACH_WHITE_VEGETATION, TerrainId.MODDABLE_SHALLOWS_1]
        self.data_triggers = self.scenario.actions.load_data_triggers()
        self.player_list = [PlayerId.ONE, PlayerId.TWO]
        self.first_flood_time = 600
        self.second_flood_time = 900
        self.third_flood_time = 1200
        self.final_flood_delay = 80
        random.seed(self.RANDOM_SEED)

    def process(self):
        CivSettings(self.scenario, self.player_list)
        layers_scenario = self.load_scenario(f'{self.input_scenario_name}_LAYERS')
        for tile in layers_scenario.new.area().select_entire_map().to_coords(as_terrain=True):
            if tile.layer in self.flood_layers:
                self.map_manager.get_tile(tile.x, tile.y).layer = tile.layer
        damage_flags = self.trigger_manager.add_trigger("Damage Flags", enabled=True, looping=True)
        damage_flags.new_condition.timer(5)
        damage_flags.new_effect.damage_object(
            source_player=PlayerId.GAIA,
            object_list_unit_id=self.SMOKE_FLAG,
            quantity=1
        )
        module_dir = Path(__file__).parent
        xs_path = module_dir / "three_gorges.xs"
        self.xs_manager.add_script(str(xs_path))
        buildings_land_and_beach = self.trigger_manager.add_trigger("Set Buildings on Land and Beach")
        buildings_land_and_beach.new_effect.script_call(message="buildings_on_land_and_beach();")
        flood_factory = FloodFactory(self.scenario, self.player_list)
        first_waterfall_dict, second_waterfall_dict, third_waterfall_dict = {}, {}, {}
        for i, waterfall_dict in enumerate([first_waterfall_dict, second_waterfall_dict, third_waterfall_dict]):
            for j, key in enumerate([f"waterfall{i + 1}_r2l", f"waterfall{i + 1}_l2r", f"waterfall{i + 1}_d"]):
                if key in self.data_triggers.tiles:
                    waterfall_dict[j] = self.data_triggers.tiles[key]
        replace_barricades = self.trigger_manager.add_trigger("Replace Barricades")
        replace_barricades.new_condition.timer(2)
        replace_barricades.new_effect.replace_object(
            source_player=PlayerId.GAIA,
            target_player=PlayerId.GAIA,
            object_list_unit_id=BuildingInfo.BARRICADE_A.ID,
            object_list_unit_id_2=OtherInfo.FLAG_A.ID
        )
        replace_barricades.new_effect.replace_object(
            source_player=PlayerId.GAIA,
            target_player=PlayerId.GAIA,
            object_list_unit_id=BuildingInfo.BARRICADE_D.ID,
            object_list_unit_id_2=OtherInfo.FLAG_B.ID
        )
        initial_tiles = [self.map_manager.get_tile(tile.x, tile.y) for tile in self.data_triggers.tiles["init_flood"]]
        first_flood_trigger = flood_factory.generate_flood(initial_tiles, self.limit_terrains, False, first_waterfall_dict, layer_mask=[TerrainId.WATER_AZURE], kill=False)
        second_flood_trigger = flood_factory.generate_flood(initial_tiles, self.limit_terrains, False, second_waterfall_dict, layer_mask=[TerrainId.WATER_AZURE, TerrainId.WATER_GREEN], kill=False)
        third_flood_trigger = flood_factory.generate_flood(initial_tiles, self.limit_terrains, False, third_waterfall_dict, layer_mask=[TerrainId.WATER_AZURE, TerrainId.WATER_GREEN, TerrainId.WATER_YELLOW_DEEP], kill=True)
        final_flood_trigger = self.trigger_manager.add_trigger("Final Flood", enabled=True)
        fish_trigger = self.trigger_manager.add_trigger("Fish", enabled=False)
        initial_timer = self.trigger_manager.add_trigger("Initial Timer")
        initial_timer.new_effect.display_timer(
            timer=0,
            reset_timer=1,
            display_time=self.third_flood_time,
            time_unit=TimeUnit.MINUTES_AND_SECONDS,
            message="Time until the dams collapse: %d",
        )
        first_flood_trigger.new_condition.timer(self.first_flood_time)
        second_flood_trigger.new_condition.timer(self.second_flood_time)
        third_flood_trigger.new_condition.timer(self.third_flood_time)
        final_flood_trigger.new_condition.timer(self.third_flood_time + self.final_flood_delay)
        first_flood_trigger.new_effect.display_instructions(
            message="The dams are weakening and some water is starting to come in!! Be careful, consider moving to higher ground.",
            display_time=30,
            source_player=PlayerId.GAIA,
            object_list_unit_id=BuildingInfo.BARRICADE_A.ID,
            sound_name="first_flood"
        )
        second_flood_trigger.new_effect.display_instructions(
            message="The water keeps coming in and has greatly weakened the dams!! They won’t hold much longer!!",
            display_time=30,
            source_player=PlayerId.GAIA,
            object_list_unit_id=BuildingInfo.BARRICADE_A.ID,
            sound_name="second_flood"
        )
        third_flood_trigger.new_effect.display_instructions(
            message="The dams have collapsed, the flooding is inevitable!! Flee to higher ground immediately!!",
            display_time=30,
            source_player=PlayerId.GAIA,
            object_list_unit_id=BuildingInfo.BARRICADE_A.ID,
            sound_name="third_flood"
        )
        third_flood_trigger.new_effect.script_call(message="buildings_on_land_no_beach();")
        first_flood_trigger.new_effect.modify_attribute(
            source_player=PlayerId.GAIA,
            object_list_unit_id=flood_factory.WARNING_WATER_BRIDGE,
            object_attributes=ObjectAttribute.FOUNDATION_TERRAIN,
            operation=Operation.SET,
            quantity=TerrainId.MODDABLE_GRASS_1,
        )
        second_flood_trigger.new_effect.modify_attribute(
            source_player=PlayerId.GAIA,
            object_list_unit_id=flood_factory.WARNING_WATER_BRIDGE,
            object_attributes=ObjectAttribute.FOUNDATION_TERRAIN,
            operation=Operation.SET,
            quantity=TerrainId.MODDABLE_GRASS_2,
        )
        third_flood_trigger.new_effect.kill_object(
            source_player=PlayerId.GAIA,
            object_list_unit_id=OtherInfo.FLAG_A.ID
        )
        third_flood_trigger.new_effect.kill_object(
            source_player=PlayerId.GAIA,
            object_list_unit_id=OtherInfo.FLAG_B.ID
        )
        final_flood_trigger.new_effect.script_call(message="units_land_no_beach();")
        final_flood_trigger.new_effect.remove_object(
            object_list_unit_id=FloodFactory.AURA_DAMAGE_UNIT,
            source_player=PlayerId.GAIA
        )
        final_flood_trigger.new_effect.activate_trigger(fish_trigger.trigger_id)

        beach_shores = self.trigger_manager.add_trigger("Beach Shores")
        beach_shores.new_condition.timer(2)
        fish_positions = []
        min_fish_dist = 3

        for tile in self.scenario.new.area().select_entire_map().to_coords(as_terrain=True):
            if tile.terrain_id == TerrainId.BEACH:
                tile.terrain_id = TerrainId.MODDABLE_SHALLOWS_1
                beach_shores.new_effect.create_object(
                    source_player=PlayerId.GAIA,
                    object_list_unit_id=FloodFactory.BEACH_BRIDGE,
                    location_x=tile.x,
                    location_y=tile.y
                )
            if tile.terrain_id in [TerrainId.BEACH_VEGETATION, TerrainId.BEACH_WET_GRAVEL, TerrainId.FOREST_REEDS_BEACH]:
                fish_too_close = any(
                    math.hypot(tile.x - fx, tile.y - fy) < min_fish_dist
                    for fx, fy in fish_positions
                )
                if not fish_too_close and random.random() < 0.05:
                    fish_trigger.new_effect.create_object(
                        source_player=PlayerId.GAIA,
                        object_list_unit_id=OtherInfo.FISH_SALMON.ID,
                        location_x=tile.x,
                        location_y=tile.y,
                    )
                    fish_positions.append((tile.x, tile.y))
            if tile.layer in self.flood_layers:
                tile.layer = -1
        beach_shores.new_effect.kill_object(
            object_list_unit_id=FloodFactory.BEACH_BRIDGE,
            source_player=PlayerId.GAIA
        )


if __name__ == '__main__':
    three_gorges = ThreeGorges(
        input_scenario_name=f'EDIT_THREE_GORGES_1V1',
        output_scenario_name=f'OUTPUT_THREE_GORGES_1V1'
    )
    three_gorges.convert()
