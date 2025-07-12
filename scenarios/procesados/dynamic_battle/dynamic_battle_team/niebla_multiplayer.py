from AoE2ScenarioParser.datasets.players import PlayerId
from scenarios.lib.parser_project import ParserProject
from scenarios.lib.civ_settings import CivSettings


class NieblaMultiplayer(ParserProject):

    def __init__(self, input_scenario_name: str, output_scenario_name: str):
        super().__init__(input_scenario_name, output_scenario_name)
        self.player_list = [PlayerId.ONE, PlayerId.TWO, PlayerId.THREE, PlayerId.FOUR]
        self.trigger_manager = self.scenario.trigger_manager

    def process(self):
        CivSettings(self.scenario, self.player_list, nomad_players=[False, True, False, True])


if __name__ == '__main__':
    niebla_class = NieblaMultiplayer(
        input_scenario_name=f'EDIT_FOG_2v2',
        output_scenario_name=f'OUTPUT_FOG_2V2'
    )
    niebla_class.convert()
