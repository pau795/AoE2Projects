from AoE2ScenarioParser.datasets.players import PlayerId

from scenarios.lib.parser_project import ParserProject
from scenarios.lib.civ_settings import CivSettings
from scenarios.lib.random_spawn import RandomSpawn
from scenarios.lib.west_train import WestTrainFactory


class WestTrain(ParserProject):
    RS_ZONE_RELATION = {
        PlayerId.ONE: {
            "zone1": {
                PlayerId.TWO: "zone2",
            },
            "zone2": {
                PlayerId.TWO: "zone1",
            },
        }
    }

    def __init__(self, input_scenario_name: str, output_scenario_name: str):
        super().__init__(input_scenario_name, output_scenario_name)
        self.player_list = [PlayerId.ONE, PlayerId.TWO]
        self.trigger_manager = self.scenario.trigger_manager
        self.data_triggers = self.scenario.actions.load_data_triggers()

    def process(self):
        RandomSpawn(self.scenario, self.data_triggers, self.player_list, self.RS_ZONE_RELATION)
        CivSettings(self.scenario, self.player_list)
        WestTrainFactory(self.scenario, train_player=PlayerId.THREE)


if __name__ == '__main__':
    west_train_class = WestTrain(
        input_scenario_name=f'EDIT_WILD_WEST_TRAIN_1V1',
        output_scenario_name=f'OUTPUT_WILD_WEST_TRAIN_1V1'
    )
    west_train_class.convert()
