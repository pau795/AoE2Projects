from AoE2ScenarioParser.datasets.buildings import BuildingInfo
from AoE2ScenarioParser.datasets.players import PlayerId
from AoE2ScenarioParser.datasets.trigger_lists import ActionType, ObjectAttribute, Operation

from scenarios.lib.parser_project import ParserProject
from scenarios.lib.civ_settings import CivSettings
from scenarios.lib.unit_modifier import UnitModifier


class Caves(ParserProject):

    def __init__(self, input_scenario_name: str, output_scenario_name: str):
        super().__init__(input_scenario_name, output_scenario_name)
        self.player_list = [PlayerId.ONE, PlayerId.TWO, PlayerId.THREE, PlayerId.FOUR, PlayerId.FIVE, PlayerId.SIX, PlayerId.SEVEN, PlayerId.EIGHT]
        self.trigger_manager = self.scenario.trigger_manager
        self.unit_manager = self.scenario.unit_manager
        self.trigger_data = self.scenario.actions.load_data_triggers()

    def process(self):
        CivSettings(self.scenario, self.player_list)
        cave_list = [v for k, v in self.trigger_data.areas.items() if k.startswith('cave')]
        (UnitModifier(self.scenario, BuildingInfo.WOODEN_BRIDGE_A_MIDDLE.ID, PlayerId.GAIA)
         .modify_attribute(ObjectAttribute.FOUNDATION_TERRAIN, Operation.SET, -2)
         .modify_attribute(ObjectAttribute.FOUNDATION_TERRAIN, Operation.DIVIDE, -2)
         .modify_attribute(ObjectAttribute.STANDING_GRAPHIC, Operation.SET, 0)
         .create_triggers()
         )

        for i, cave in enumerate(cave_list):
            print(f'{cave[0].get_dimensions()} {cave[1].get_dimensions()}')
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
                    object_list_unit_id=BuildingInfo.WOODEN_BRIDGE_A_MIDDLE.ID
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


if __name__ == '__main__':
    cave_class = Caves(
        input_scenario_name=f'EDIT_CAVES_4V4',
        output_scenario_name=f'OUTPUT_CAVES_4V4'
    )
    cave_class.convert()
