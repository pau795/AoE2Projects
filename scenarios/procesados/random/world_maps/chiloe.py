from AoE2ScenarioParser.datasets.players import PlayerId

from scenarios.lib.nomad_start import NomadStart
from scenarios.lib.parser_project import ParserProject


class Chiloe(ParserProject):

    def __init__(self, input_scenario_name: str, output_scenario_name: str):
        super().__init__(input_scenario_name, output_scenario_name)
        self.player_list = [PlayerId.ONE, PlayerId.TWO]

    def process(self):
        try:
            trigger_manager = self.scenario.trigger_manager
            trigger_data = self.scenario.actions.load_data_triggers()
            NomadStart(trigger_manager, trigger_data, self.player_list)
        except Exception as e:
            raise e


chiloe = Chiloe(
    input_scenario_name='CHILOE_EDITAR',
    output_scenario_name='CHILOE_output',
)
chiloe.convert()
