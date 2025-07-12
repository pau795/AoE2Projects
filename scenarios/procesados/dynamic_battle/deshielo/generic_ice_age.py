import math
import random
from AoE2ScenarioParser.datasets.other import OtherInfo
from AoE2ScenarioParser.datasets.players import PlayerId
from AoE2ScenarioParser.datasets.terrains import TerrainId

from scenarios.lib.parser_project import ParserProject


class IceAge(ParserProject):

    def __init__(self, input_scenario_name: str, output_scenario_name: str):
        super().__init__(input_scenario_name, output_scenario_name)
        self.trigger_manager = self.scenario.trigger_manager
        self.unit_manager = self.scenario.unit_manager
        self.map_manager = self.scenario.map_manager
        self.player_list = [PlayerId.ONE, PlayerId.TWO]

    def process(self):
        self.freeze()
        self.create_trees()
        self.unfreeze()

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

    def create_trees(self):
        area = self.scenario.new.area().select_entire_map()
        first_stage_time = 520
        second_stage_time = 850
        third_stage_time = 1350
        first_forest = self.trigger_manager.add_trigger("Bosque Primera Fase", enabled=True, looping=False)
        first_forest.new_condition.timer(timer=first_stage_time)
        second_forest = self.trigger_manager.add_trigger("Bosque Segunda Fase", enabled=True, looping=False)
        second_forest.new_condition.timer(timer=second_stage_time)
        third_forest = self.trigger_manager.add_trigger("Bosque Tercera Fase", enabled=True, looping=False)
        third_forest.new_condition.timer(timer=third_stage_time)
        for tile in area.to_coords(as_terrain=True):
            if tile.layer == TerrainId.FARM:
                if len(first_forest.effects) > 150:
                    first_stage_time += 2
                    first_forest = self.trigger_manager.add_trigger("Bosque Primera Fase", enabled=True, looping=False)
                    first_forest.new_condition.timer(timer=first_stage_time)
                first_forest.new_effect.create_object(
                    source_player=PlayerId.GAIA,
                    object_list_unit_id=OtherInfo.TREE_OAK_AUTUMN_SNOW.ID,
                    location_x=tile.x,
                    location_y=tile.y,
                )
                tile.layer = -1
            elif tile.layer == TerrainId.ROAD:
                if len(second_forest.effects) > 150:
                    second_stage_time += 2
                    second_forest = self.trigger_manager.add_trigger("Bosque Segunda Fase", enabled=True, looping=False)
                    second_forest.new_condition.timer(timer=second_stage_time)
                second_forest.new_effect.create_object(
                    source_player=PlayerId.GAIA,
                    object_list_unit_id=OtherInfo.TREE_DRAGON.ID,
                    location_x=tile.x,
                    location_y=tile.y,
                )
                tile.layer = -1
            elif tile.layer == TerrainId.ICE:
                if len(third_forest.effects) > 150:
                    third_stage_time += 2
                    third_forest = self.trigger_manager.add_trigger("Bosque Tercera Fase", enabled=True, looping=False)
                    third_forest.new_condition.timer(timer=third_stage_time)
                third_forest.new_effect.create_object(
                    source_player=PlayerId.GAIA,
                    object_list_unit_id=OtherInfo.TREE_PALM_FOREST.ID,
                    location_x=tile.x,
                    location_y=tile.y,
                )
                tile.layer = -1

    def unfreeze(self):
        elevation_tiles = {}
        unfreeze_delay = 600
        for tile in self.scenario.new.area().select_entire_map().to_coords(as_terrain=True):
            if tile.elevation not in elevation_tiles:
                elevation_tiles[tile.elevation] = []
            elevation_tiles[tile.elevation].append(tile)
        sorted_elevation_tiles = dict(sorted(elevation_tiles.items()))
        for elevation, tile_list in sorted_elevation_tiles.items():
            unfreeze_trigger = self.trigger_manager.add_trigger(f"Unfreeze Elevation {elevation}", enabled=True, looping=False)
            kill_trigger = self.trigger_manager.add_trigger(f"Kill Water Units", enabled=True, looping=False)
            kill_trigger.new_condition.timer(timer=unfreeze_delay)
            unfreeze_trigger.new_condition.timer(timer=unfreeze_delay)
            for tile in tile_list:
                unfreeze_trigger.new_effect.remove_object(
                    source_player=PlayerId.GAIA,
                    object_list_unit_id=OtherInfo.ICE_NAVIGABLE.ID,
                    area_x1=tile.x,
                    area_y1=tile.y,
                    area_x2=tile.x,
                    area_y2=tile.y
                )
                if tile.terrain_id == TerrainId.WATER_AZURE:
                    for player in self.player_list:
                        kill_trigger.new_effect.kill_object(
                            source_player=player,
                            area_x1=tile.x,
                            area_y1=tile.y,
                            area_x2=tile.x,
                            area_y2=tile.y
                        )
                if len(unfreeze_trigger.effects) > 25:
                    unfreeze_delay += 2
                    unfreeze_trigger = self.trigger_manager.add_trigger(f"Unfreeze Elevation {elevation}", enabled=True, looping=False)
                    unfreeze_trigger.new_condition.timer(timer=unfreeze_delay)
                    if tile.terrain_id == TerrainId.WATER_AZURE:
                        kill_trigger = self.trigger_manager.add_trigger(f"Kill Water Units", enabled=True, looping=False)
                        kill_trigger.new_condition.timer(timer=unfreeze_delay)
            unfreeze_delay += 2


ice_age = IceAge(
    input_scenario_name='ICE AGE MOUNTAIN_fixed',
    output_scenario_name='ICE AGE MOUNTAIN_output'
)
ice_age.convert()
