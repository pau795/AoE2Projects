from AoE2ScenarioParser.datasets.players import PlayerId

from scenarios.lib.parser_project import ParserProject
from scenarios.lib.civ_settings import CivSettings


class Armageddon(ParserProject):

    def __init__(self, input_scenario_name: str, output_scenario_name: str):
        super().__init__(input_scenario_name, output_scenario_name)
        self.player_list = [PlayerId.ONE, PlayerId.TWO, PlayerId.THREE, PlayerId.FOUR, PlayerId.FIVE, PlayerId.SIX]

    def process(self):
        CivSettings(self.scenario, self.player_list)


if __name__ == '__main__':
    armageddon_class = Armageddon(
        input_scenario_name=f'EDIT_ARMAGEDDON_3v3',
        output_scenario_name=f'OUTPUT_ARMAGEDDON_3V3'
    )
    armageddon_class.convert()
