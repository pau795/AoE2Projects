import itertools
from collections import deque

from AoE2ScenarioParser.datasets.buildings import BuildingInfo
from AoE2ScenarioParser.datasets.other import OtherInfo
from AoE2ScenarioParser.datasets.players import PlayerId
from AoE2ScenarioParser.datasets.terrains import TerrainId
from AoE2ScenarioParser.datasets.trigger_lists import ObjectAttribute, Operation, ObjectState
from AoE2ScenarioParser.objects.data_objects.terrain_tile import TerrainTile
from AoE2ScenarioParser.objects.data_objects.trigger import Trigger
from AoE2ScenarioParser.objects.support.area import Area
from AoE2ScenarioParser.objects.support.tile import Tile
from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario

from scenarios.lib.unit_modifier import UnitModifier


class FloodFactory:

    BEACH_BRIDGE = BuildingInfo.WOODEN_BRIDGE_A_MIDDLE.ID
    SHALLOW_WATER_BRIDGE = BuildingInfo.WOODEN_BRIDGE_B_MIDDLE.ID
    AZURE_WATER_BRIDGE = BuildingInfo.WOODEN_BRIDGE_B_BOTTOM.ID

    def __init__(self, scenario: AoE2DEScenario, player_list: list[int]):
        self.scenario = scenario
        self.map_manager = scenario.map_manager
        self.trigger_manager = scenario.trigger_manager
        self.player_list = player_list

    def generate_flood(self, init_tiles: list[TerrainTile], limit_terrains: list[int], stop_on_elevation: bool = True,
                       waterfall_tiles: dict[int, list[Tile]] = None, layer_mask: list[int] = None, kill: bool = False) -> Trigger:
        delay = 2
        trigger_list = []
        visited_tiles = set()
        tile_queue = deque([(tile, 0) for tile in init_tiles])
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
            invalid_neighbor = False
            for dx, dy in itertools.product((-1, 0, 1), repeat=2):
                if (dx == 0 and dy == 0) or not (0 <= current_tile.x + dx < self.map_manager.map_width) or not (0 <= current_tile.y + dy < self.map_manager.map_height):
                    continue
                new_tile = self.map_manager.get_tile(current_tile.x + dx, current_tile.y + dy)
                if not stop_on_elevation or new_tile.elevation == 0:
                    if new_tile not in visited_tiles and new_tile.terrain_id not in limit_terrains and (layer_mask is None or new_tile.layer in layer_mask):
                        tile_queue.append((new_tile, distance + 1))
                        visited_tiles.add(new_tile)
                else:
                    invalid_neighbor = True
            bridge_unit = self.AZURE_WATER_BRIDGE if not kill else (self.BEACH_BRIDGE if stop_on_elevation and invalid_neighbor else self.SHALLOW_WATER_BRIDGE)
            if kill:
                for player in self.player_list + [PlayerId.GAIA]:
                    bridge_trigger.new_effect.kill_object(
                        source_player=player,
                        area_x1=current_tile.x,
                        area_y1=current_tile.y,
                        area_x2=current_tile.x,
                        area_y2=current_tile.y,
                    )
                    for state in [ObjectState.ALIVE, ObjectState.ALMOST_ALIVE, ObjectState.FOUNDATION]:
                        bridge_trigger.new_effect.remove_object(
                            source_player=player,
                            object_state=state,
                            area_x1=current_tile.x,
                            area_y1=current_tile.y,
                            area_x2=current_tile.x,
                            area_y2=current_tile.y,
                        )
                for state in [ObjectState.DEAD, ObjectState.ALMOST_ALIVE, ObjectState.RESOURCE, ObjectState.DYING, ObjectState.ALIVE]:
                    bridge_trigger.new_effect.remove_object(
                        source_player=PlayerId.GAIA,
                        object_state=state,
                        area_x1=current_tile.x,
                        area_y1=current_tile.y,
                        area_x2=current_tile.x,
                        area_y2=current_tile.y,
                    )
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
        if waterfall_tiles is not None:
            for facet, tiles in waterfall_tiles.items():
                for tile in tiles:
                    start_flood.new_effect.create_object(
                        source_player=PlayerId.GAIA,
                        object_list_unit_id=OtherInfo.WATERFALL_OVERLAY.ID,
                        location_x=tile.x,
                        location_y=tile.y,
                        facet=facet
                    )
        for trigger in trigger_list:
            start_flood.new_effect.activate_trigger(trigger.trigger_id)
        return start_flood
