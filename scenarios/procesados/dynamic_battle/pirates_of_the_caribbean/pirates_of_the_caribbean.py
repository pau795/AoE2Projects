from AoE2ScenarioParser.datasets.players import PlayerId
from scenarios.lib.parser_project import ParserProject
from scenarios.lib.civ_settings import CivSettings


class PiratesOfTheCaribbean(ParserProject):

    def __init__(self, input_scenario_name: str, output_scenario_name: str):
        super().__init__(input_scenario_name, output_scenario_name)
        self.player_list = [PlayerId.ONE, PlayerId.TWO]
        self.trigger_manager = self.scenario.trigger_manager

    def process(self):
        CivSettings(self.scenario, self.player_list)


if __name__ == '__main__':
    pirates_class = PiratesOfTheCaribbean(
        input_scenario_name=f'EDIT_PIRATES_OF_THE_CARIBBEAN_1V1',
        output_scenario_name=f'OUTPUT_PIRATES_OF_THE_CARIBBEAN_1V1'
    )
    pirates_class.convert()
