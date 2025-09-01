from AoE2ScenarioParser.datasets.buildings import BuildingInfo
from AoE2ScenarioParser.datasets.players import PlayerId
from AoE2ScenarioParser.datasets.trigger_lists import ObjectAttribute, Operation, ActionType
from AoE2ScenarioParser.objects.support.area import Area
from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario

from scenarios.lib.unit_modifier import UnitModifier


class CaveFactory:

    def __init__(self, scenario: AoE2DEScenario, player_list: list[PlayerId]):
        self.scenario = scenario
        self.trigger_manager = scenario.trigger_manager
        self.player_list = player_list

    def caves_stats(self):
        (UnitModifier(self.scenario, BuildingInfo.BRIDGE_PIECE_AB_END_A.ID, PlayerId.GAIA)
         .modify_attribute(ObjectAttribute.FOUNDATION_TERRAIN, Operation.SET, -2)
         .modify_attribute(ObjectAttribute.FOUNDATION_TERRAIN, Operation.DIVIDE, -2)
         .modify_attribute(ObjectAttribute.STANDING_GRAPHIC, Operation.SET, 0)
         .create_triggers()
         )

    def generate_caves(self, cave_list: list[list[Area]]):
        for i, cave in enumerate(cave_list):
            if cave[0].get_dimensions() != cave[1].get_dimensions():
                raise ValueError(f'Cave {i} has different dimensions: {cave[0].get_dimensions()} {cave[1].get_dimensions()}')
            cave_area = cave[0]
            teleport_area = cave[1]
            destination = cave[2].get_center()
            create_bridges = self.trigger_manager.add_trigger(f'cave{i} bridges', enabled=True)
            create_bridges.new_condition.timer(2)
            for tile in cave_area.to_coords():
                create_bridges.new_effect.create_object(
                    source_player=PlayerId.GAIA,
                    location_x=tile.x,
                    location_y=tile.y,
                    object_list_unit_id=BuildingInfo.BRIDGE_PIECE_AB_END_A.ID
                )
            teleport_trigger = self.trigger_manager.add_trigger(f'cave{i}', enabled=True, looping=True)
            move_trigger = self.trigger_manager.add_trigger(f'cave{i} move', enabled=True, looping=True)
            for player in self.player_list:
                for cave_tile, teleport_tile in zip(cave_area.to_coords(), teleport_area.to_coords()):
                    teleport_trigger.new_effect.teleport_object(
                        source_player=player,
                        area_x1=cave_tile.x,
                        area_y1=cave_tile.y,
                        area_x2=cave_tile.x,
                        area_y2=cave_tile.y,
                        location_x=teleport_tile.x,
                        location_y=teleport_tile.y
                    )
                move_trigger.new_effect.task_object(
                    source_player=player,
                    area_x1=teleport_area.x1,
                    area_y1=teleport_area.y1,
                    area_x2=teleport_area.x2,
                    area_y2=teleport_area.y2,
                    location_x=int(destination[0]),
                    location_y=int(destination[1]),
                    action_type=ActionType.MOVE
                )
