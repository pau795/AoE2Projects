from AoE2ScenarioParser.datasets.players import PlayerId
from scenarios.lib.parser_project import ParserProject
from scenarios.lib.civ_settings import CivSettings
from scenarios.lib.twister_factory import TwisterFactory


class Twister(ParserProject):

    def __init__(self,
                 steam_id,
                 input_scenario_name: str,
                 output_scenario_name: str):
        super().__init__(steam_id, input_scenario_name, output_scenario_name)
        self.radius = 20
        self.arms = 10
        self.drag_radius = 12
        self.inner_radius = 7
        self.spawn_times = [60, 100, 150, 200]
        self.duration_times = [30, 45, 60, 75]
        self.twister_sound = 'twister'
        self.sound_delay = 200
        self.player_list = [PlayerId.ONE, PlayerId.TWO]

    def process(self):
        trigger_data = self.scenario.actions.load_data_triggers()
        twister_tiles = trigger_data.tiles["twister"]

        CivSettings(self.scenario, self.player_list)

        factory = TwisterFactory(
            scenario=self.scenario,
            player_list=self.player_list,
            twister_sound_name=self.twister_sound,
            sound_delay=self.sound_delay
        )
        factory.twister_stats()
        factory.twister_sound()
        for twister_center in twister_tiles:
            factory.spawn_tornado(
                center=twister_center,
                radius=self.radius,
                arms=self.arms,
                drag_radius=self.drag_radius,
                inner_radius=self.inner_radius,
                spawn_times=self.spawn_times,
                duration_times=self.duration_times
            )


if __name__ == '__main__':
    twister = Twister(
        input_scenario_name='twister',
        output_scenario_name='twister_output',

    )
    twister.convert()
