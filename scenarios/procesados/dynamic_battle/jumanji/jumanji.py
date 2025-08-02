from AoE2ScenarioParser.datasets.players import PlayerId

from scenarios.lib.parser_project import ParserProject


class Jumanji(ParserProject):

    def __init__(self, input_scenario_name: str, output_scenario_name: str):
        super().__init__(input_scenario_name, output_scenario_name)
        self.player_list = [PlayerId.ONE, PlayerId.TWO]
        self.trigger_manager = self.scenario.trigger_manager

    def process(self):
        xs_manager = self.scenario.xs_manager
        xs_manager.add_script(xs_file_path="jumanji.xs")


if __name__ == '__main__':
    jumanji_class = Jumanji(
        input_scenario_name=f'JUMANJI_DYNAMIC',
        output_scenario_name=f'OUTPUT_JUMANJI_DYNAMIC'
    )
    jumanji_class.convert()
