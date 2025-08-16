from AoE2ScenarioParser.datasets.players import PlayerId
from scenarios.lib.parser_project import ParserProject
from scenarios.lib.civ_settings import CivSettings
from scenarios.lib.tsunami_factory import TsunamiFactory


class TsunamiRemake(ParserProject):

    def __init__(self, input_scenario_name: str, output_scenario_name: str):
        super().__init__(input_scenario_name, output_scenario_name)
        data_triggers = self.scenario.actions.load_data_triggers()
        self.tsunami_tiles = data_triggers.tiles['tsunami']
        self.player_list = [PlayerId.ONE, PlayerId.TWO]
        self.trigger_manager = self.scenario.trigger_manager

    def process(self):
        tsunami_factory = TsunamiFactory(
            scenario=self.scenario,
            tsunami_sound_name='sirena60',
            tsunami_speed=2,
            tsunami_unit_damage=30,
            player_list=self.player_list
        )
        tsunami_factory.tsunami_stats()
        tsunami_factory.config_tsunami(
            tile_list=self.tsunami_tiles,
            amplitude=8,
            thickness=1.2,
            wave_delay=15,
            tsunami_periods=[60]
        )
        CivSettings(self.scenario, self.player_list)


if __name__ == '__main__':
    tsunami_remake = TsunamiRemake(
        input_scenario_name='tsunami_remake',
        output_scenario_name='tsunami_remake_output',
    )
    tsunami_remake.convert()
