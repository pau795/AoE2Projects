from AoE2ScenarioParser.datasets.players import PlayerId

from scenarios.lib.nomad_start import NomadStart
from scenarios.lib.parser_project import ParserProject


class Pascua(ParserProject):

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


Pascua = Pascua(
    input_scenario_name='pascua_editar',
    output_scenario_name='pascua_output',
)
Pascua.convert()
