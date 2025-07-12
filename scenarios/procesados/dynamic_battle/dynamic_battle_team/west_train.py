from AoE2ScenarioParser.datasets.players import PlayerId

from scenarios.lib.parser_project import ParserProject
from scenarios.lib.civ_settings import CivSettings


class WestTrain(ParserProject):

    def __init__(self, input_scenario_name: str, output_scenario_name: str):
        super().__init__(input_scenario_name, output_scenario_name)
        self.player_list = [PlayerId.ONE, PlayerId.TWO, PlayerId.THREE, PlayerId.FOUR, PlayerId.FIVE, PlayerId.SIX]
        self.trigger_manager = self.scenario.trigger_manager

    def process(self):
        xs_manager = self.scenario.xs_manager
        xs_manager.add_script(xs_file_path="west_train.xs")
        CivSettings(self.scenario, self.player_list)


if __name__ == '__main__':
    west_train_class = WestTrain(
        input_scenario_name=f'EDIT_WILD_WEST_TRAIN_3V3',
        output_scenario_name=f'OUTPUT_WILD_WEST_TRAIN_3V3'
    )
    west_train_class.convert()
