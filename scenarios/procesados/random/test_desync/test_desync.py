from AoE2ScenarioParser.datasets.other import OtherInfo
from AoE2ScenarioParser.datasets.players import PlayerId

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
        xs_path = 'C:\\Users\\pau_7\\OneDrive\\Documentos\\AoE2 Data\\projects\\AoE2 Projects\\scenarios\\lib\\xs\\bridge_stats.xs'
        self.xs_manager.add_script(xs_file_path=xs_path)
        xs_trigger = self.trigger_manager.add_trigger("XS CALL BRIDGE_STATS")
        xs_trigger.new_effect.script_call(message="bridge_stats();")
        create_rocks = self.trigger_manager.add_trigger('create rocks', enabled=True)
        create_rocks.new_condition.timer(3)
        horizontal_chain_fixed_unit = OtherInfo.ROCK_FORMATION_1.ID
        vertical_chain_fixed_unit = OtherInfo.ROCK_FORMATION_2.ID
        for area in self.data_triggers.areas['shallows']:
            unit = vertical_chain_fixed_unit if area.get_width() > area.get_height() else horizontal_chain_fixed_unit
            for i, tile in enumerate(area.to_coords()):
                if i % 2 != 0:
                    create_rocks.new_effect.create_object(
                        source_player=PlayerId.GAIA,
                        object_list_unit_id=unit,
                        location_x=tile.x,
                        location_y=tile.y)


if __name__ == '__main__':
    desync_class = Desync(        
        input_scenario_name=f'test_desync',
        output_scenario_name=f'test_desync_output'
    )
    desync_class.convert()
