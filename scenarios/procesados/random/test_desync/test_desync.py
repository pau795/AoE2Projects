from AoE2ScenarioParser.datasets.other import OtherInfo
from AoE2ScenarioParser.datasets.players import PlayerId
from AoE2ScenarioParser.datasets.terrains import TerrainId
from AoE2ScenarioParser.datasets.trigger_lists import ObjectAttribute, Operation
from AoE2ScenarioParser.datasets.units import UnitInfo
from AoE2ScenarioParser.objects.support.area import Area
from AoE2ScenarioParser.objects.support.tile import Tile

from scenarios.lib.parser_project import ParserProject


class Desync(ParserProject):

    def __init__(self, input_scenario_name: str, output_scenario_name: str):
        super().__init__(input_scenario_name, output_scenario_name)
        self.trigger_manager = self.scenario.trigger_manager
        self.map_manager = self.scenario.map_manager
        self.unit_manager = self.scenario.unit_manager
        self.xs_manager = self.scenario.xs_manager
        self.data_triggers = self.scenario.actions.load_data_triggers()

    def process(self):
        center = self.scenario.new.area().select_entire_map().get_center()
        center_tile = Tile(int(center[0]), int(center[1]))
        area = self.scenario.new.area()
        area.center(center_tile.x, center_tile.y)
        radius = 15
        area.expand(radius)
        for tile in area.to_coords(as_terrain=True):
            dx = tile.x - center_tile.x
            dy = tile.y - center_tile.y
            distance_squared = dx * dx + dy * dy

            # Check if point is within the circle
            if abs(distance_squared - (radius * radius)) < 10:
                tile.terrain_id = TerrainId.FARM

        self.unit_manager.add_unit(
            player=PlayerId.ONE,
            unit_const=UnitInfo.MILITIA.ID,
            x=center_tile.x,
            y=center_tile.y,
            z=0
        )
        stats_trigger = self.trigger_manager.add_trigger('stats trigger')
        stats_trigger.new_effect.modify_attribute(
            source_player=PlayerId.ONE,
            object_list_unit_id=UnitInfo.MILITIA.ID,
            object_attributes=ObjectAttribute.WALKING_GRAPHIC,
            operation=Operation.SET,
            quantity=9402
        )
        stats_trigger.new_effect.modify_attribute(
            source_player=PlayerId.ONE,
            object_list_unit_id=UnitInfo.MILITIA.ID,
            object_attributes=ObjectAttribute.MOVEMENT_SPEED,
            operation=Operation.SET,
            quantity=0.01
        )


if __name__ == '__main__':
    desync_class = Desync(        
        input_scenario_name=f'directional_graphic',
        output_scenario_name=f'directional_graphic_output'
    )
    desync_class.convert()
