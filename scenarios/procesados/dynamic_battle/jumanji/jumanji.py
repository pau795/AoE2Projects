from pathlib import Path

from AoE2ScenarioParser.datasets.players import PlayerId

from scenarios.lib.civ_settings import CivSettings
from scenarios.lib.parser_project import ParserProject


class Jumanji(ParserProject):

    def __init__(self, input_scenario_name: str, output_scenario_name: str):
        super().__init__(input_scenario_name, output_scenario_name)
        self.player_list = [PlayerId.ONE, PlayerId.TWO]
        self.trigger_manager = self.scenario.trigger_manager

    def process(self):
        CivSettings(self.scenario, self.player_list, delay=3)
        module_dir = Path(__file__).parent
        xs_path = module_dir / "jumanji.xs"
        self.scenario.xs_manager.add_script(str(xs_path))


if __name__ == '__main__':
    jumanji_class = Jumanji(
        input_scenario_name=f'EDIT_JUMANJI_1V1',
        output_scenario_name=f'OUTPUT_JUMANJI_1V1'
    )
    jumanji_class.convert()
