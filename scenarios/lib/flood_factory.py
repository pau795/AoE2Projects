import itertools
from collections import deque

from AoE2ScenarioParser.datasets.buildings import BuildingInfo
from AoE2ScenarioParser.datasets.other import OtherInfo
from AoE2ScenarioParser.datasets.players import PlayerId
from AoE2ScenarioParser.datasets.terrains import TerrainId
from AoE2ScenarioParser.datasets.trigger_lists import ObjectAttribute, Operation
from AoE2ScenarioParser.objects.data_objects.terrain_tile import TerrainTile
from AoE2ScenarioParser.objects.support.area import Area
from AoE2ScenarioParser.objects.support.tile import Tile
from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario

from scenarios.lib.unit_modifier import UnitModifier


class FloodFactory:

    def __init__(self, scenario: AoE2DEScenario):
        self.scenario = scenario
        self.map_manager = scenario.map_manager
        self.trigger_manager = scenario.trigger_manager

    def bridge_stats(self):
        (UnitModifier(self.scenario, BuildingInfo.WOODEN_BRIDGE_A_MIDDLE.ID, PlayerId.GAIA)
         .modify_attribute(ObjectAttribute.UNIT_SIZE_X, Operation.SET, 0)
         .modify_attribute(ObjectAttribute.UNIT_SIZE_Y, Operation.SET, 0)
         .modify_attribute(ObjectAttribute.UNIT_SIZE_Z, Operation.SET, 0)
         .modify_attribute(ObjectAttribute.DYING_GRAPHIC, Operation.SET, 5507)
         .modify_attribute(ObjectAttribute.DEAD_UNIT_ID, Operation.SET, -2)
         .modify_attribute(ObjectAttribute.DEAD_UNIT_ID, Operation.DIVIDE, 2)
         .modify_attribute(ObjectAttribute.FOUNDATION_TERRAIN, Operation.SET, TerrainId.BEACH)
         .modify_attribute(ObjectAttribute.STANDING_GRAPHIC, Operation.SET, 0)
         .create_triggers()
         )
        (UnitModifier(self.scenario, BuildingInfo.WOODEN_BRIDGE_B_MIDDLE.ID, PlayerId.GAIA)
         .modify_attribute(ObjectAttribute.UNIT_SIZE_X, Operation.SET, 0)
         .modify_attribute(ObjectAttribute.UNIT_SIZE_Y, Operation.SET, 0)
         .modify_attribute(ObjectAttribute.UNIT_SIZE_Z, Operation.SET, 0)
         .modify_attribute(ObjectAttribute.DYING_GRAPHIC, Operation.SET, 5507)
         .modify_attribute(ObjectAttribute.DEAD_UNIT_ID, Operation.SET, -2)
         .modify_attribute(ObjectAttribute.DEAD_UNIT_ID, Operation.DIVIDE, 2)
         .modify_attribute(ObjectAttribute.FOUNDATION_TERRAIN, Operation.SET, TerrainId.WATER_SHALLOW)
         .modify_attribute(ObjectAttribute.STANDING_GRAPHIC, Operation.SET, 0)
         .create_triggers()
         )

    def generate_flood(self, init_tile: TerrainTile, limit_area: Area, waterfall_tiles: list[Tile]):
        delay = 2
        trigger_list = []
        visited_tiles = set()
        tile_queue = deque([(init_tile, 0)])
        bridge_trigger = self.trigger_manager.add_trigger(name=f"Bridge {delay}", enabled=False)
        bridge_trigger.new_condition.timer(timer=delay)
        trigger_list.append(bridge_trigger)
        current_distance = 0
        while tile_queue:
            current_tile, distance = tile_queue.popleft()
            print(f'{current_tile.x}, {current_tile.y}, distance: {distance}, queue size: {len(tile_queue)}, visited: {len(visited_tiles)}')
            if distance > current_distance:
                current_distance = distance
                delay += 1
                bridge_trigger = self.trigger_manager.add_trigger(name=f"Bridge {delay}", enabled=False)
                bridge_trigger.new_condition.timer(timer=delay)
                trigger_list.append(bridge_trigger)
            slope = False
            for dx, dy in itertools.product((-1, 0, 1), repeat=2):
                if (dx == 0 and dy == 0) or not (0 <= current_tile.x + dx < self.map_manager.map_width) or not (0 <= current_tile.y + dy < self.map_manager.map_height):
                    continue
                new_tile = self.map_manager.get_tile(current_tile.x + dx, current_tile.y + dy)
                if new_tile.elevation == 0:
                    if new_tile not in visited_tiles and new_tile not in limit_area.to_coords(as_terrain=True):
                        tile_queue.append((new_tile, distance + 1))
                        visited_tiles.add(new_tile)
                else:
                    slope = True
            bridge_unit = BuildingInfo.WOODEN_BRIDGE_A_MIDDLE.ID if slope else BuildingInfo.WOODEN_BRIDGE_B_MIDDLE.ID
            bridge_trigger.new_effect.create_object(
                source_player=PlayerId.GAIA,
                object_list_unit_id=bridge_unit,
                location_x=current_tile.x,
                location_y=current_tile.y,
            )
            bridge_trigger.new_effect.kill_object(
                source_player=PlayerId.GAIA,
                object_list_unit_id=bridge_unit,
                area_x1=current_tile.x,
                area_y1=current_tile.y,
                area_x2=current_tile.x,
                area_y2=current_tile.y,
            )
        start_flood = self.trigger_manager.add_trigger(name="Start Flood", enabled=True)
        start_flood.new_condition.timer(10)
        for tile in waterfall_tiles:
            start_flood.new_effect.create_object(
                source_player=PlayerId.GAIA,
                object_list_unit_id=OtherInfo.WATERFALL_OVERLAY.ID,
                location_x=tile.x,
                location_y=tile.y,
                facet=2
            )
        for trigger in trigger_list:
            start_flood.new_effect.activate_trigger(trigger.trigger_id)
