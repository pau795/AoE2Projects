from AoE2ScenarioParser.datasets.players import PlayerId

from scenarios.lib.nomad_start import NomadStart
from scenarios.lib.parser_project import ParserProject


class LaPampa(ParserProject):

    def __init__(self, input_scenario_name: str, output_scenario_name: str, player_list: list[PlayerId]):
        super().__init__(input_scenario_name, output_scenario_name)
        self.player_list = player_list
        self.trigger_manager = self.scenario.trigger_manager
        self.trigger_data = self.scenario.actions.load_data_triggers()

    def process(self):
        NomadStart(self.trigger_manager, self.trigger_data, self.player_list)


if __name__ == '__main__':
    la_pampa_3v3 = LaPampa(
        input_scenario_name='LA PAMPA',
        output_scenario_name='LA PAMPA_3v3',
        player_list=[PlayerId.ONE, PlayerId.TWO, PlayerId.THREE, PlayerId.FOUR, PlayerId.FIVE, PlayerId.SIX]
    )
    la_pampa_3v3 .convert()

    la_pampa_4v4 = LaPampa(
        input_scenario_name='LA PAMPA',
        output_scenario_name='LA PAMPA_4v4',
        player_list=[PlayerId.ONE, PlayerId.TWO, PlayerId.THREE, PlayerId.FOUR, PlayerId.FIVE, PlayerId.SIX, PlayerId.SEVEN, PlayerId.EIGHT]
    )
    la_pampa_4v4.convert()

