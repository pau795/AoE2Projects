import random

from AoE2ScenarioParser.datasets.players import PlayerId

from scenarios.lib.civ_settings import CivSettings
from scenarios.lib.parser_project import ParserProject
from scenarios.lib.thunder_factory import ThunderFactory
from scenarios.procesados.random.desert_madness.general.teleports import players


class ThunderDunes(ParserProject):
    RANDOM_SEED = 123156

    def __init__(self, input_scenario_name: str, output_scenario_name: str):
        super().__init__(input_scenario_name, output_scenario_name)
        self.trigger_manager = self.scenario.trigger_manager
        self.data_triggers = self.scenario.actions.load_data_triggers()
        self.map_manager = self.scenario.map_manager
        self.unit_manager = self.scenario.unit_manager
        self.xs_manager = self.scenario.xs_manager
        self.player_list = [PlayerId.ONE, PlayerId.TWO]
        random.seed(self.RANDOM_SEED)

    def process(self):
        CivSettings(self.scenario, self.player_list)
        thunder_factory = ThunderFactory(
            self.scenario,
            self.player_list,
            500,
            40,
            60
        )
        thunder_factory.set_thunder_flags()
        thunder_areas = self.data_triggers.areas['thunder_dunes']
        display_variables = self.trigger_manager.add_trigger("Display Variables")
        display_variables.display_on_screen = 1
        display_variables.new_condition.player_defeated(source_player=PlayerId.ONE)
        for i, area in enumerate(thunder_areas):
            self.trigger_manager.add_variable(f'thunder_dune_{i}', i)
            display_variables.short_description += f'Thunder Dune {i}: <thunder_dune_{i}>\n'
            thunder_factory.set_thunder_zone(area, i)
        thunder_factory.set_thunder_flag_damage()


if __name__ == '__main__':
    thunder_dunes_class = ThunderDunes(
        input_scenario_name='EDIT_THUNDER_DUNES_1V1',
        output_scenario_name='OUTPUT_THUNDER_DUNES_1V1'
    )
    thunder_dunes_class.convert()
