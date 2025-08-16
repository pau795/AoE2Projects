from AoE2ScenarioParser.datasets.players import PlayerId

from scenarios.lib.civ_settings import CivSettings
from scenarios.lib.nomad_start import NomadStart
from scenarios.lib.parser_project import ParserProject


class NomadStartScenario(ParserProject):

    def __init__(self, input_scenario_name: str, output_scenario_name: str):
        super().__init__(input_scenario_name, output_scenario_name)
        self.player_list = [PlayerId.ONE, PlayerId.TWO]
        self.trigger_manager = self.scenario.trigger_manager
        self.trigger_data = self.scenario.actions.load_data_triggers()

    def process(self):
        NomadStart(self.trigger_manager, self.trigger_data, self.player_list)


if __name__ == '__main__':
    nomad_start_class = NomadStartScenario(
        input_scenario_name=f'TEMPLATE',
        output_scenario_name=f'OUTPUT_TEMPLATE'
    )
    nomad_start_class.convert()
