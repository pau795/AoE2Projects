from AoE2ScenarioParser.datasets.players import PlayerId

from scenarios.lib.earthquake_factory import EarthquakeFactory
from scenarios.lib.parser_project import ParserProject
from scenarios.lib.civ_settings import CivSettings


class AllMapEarthquake(ParserProject):

    def __init__(self, input_scenario_name: str, output_scenario_name: str):
        super().__init__(input_scenario_name, output_scenario_name)

    def process(self):
        trigger_manager = self.scenario.trigger_manager
        data_triggers = self.scenario.actions.load_data_triggers()
        earthquake1_areas = data_triggers.areas['earthquake 1']
        earthquake2_areas = data_triggers.areas['earthquake 2']
        players = [PlayerId.ONE, PlayerId.TWO]
        EarthquakeFactory(
            scenario=self.scenario,
            initial_delay=900,
            warning_delay=30,
            earthquake_duration=30,
            period_list=[240],
            damage=30,
            area_list=earthquake1_areas,
            crack_sound='grietas',
            earthquake_sound='terremoto',
            player_list=players
        )
        EarthquakeFactory(
            scenario=self.scenario,
            initial_delay=1200,
            warning_delay=30,
            earthquake_duration=30,
            period_list=[360, 420, 480, 540, 600],
            damage=30,
            area_list=earthquake2_areas,
            crack_sound='grietas',
            earthquake_sound='terremoto',
            player_list=players
        )
        CivSettings(self.scenario, players)


if __name__ == '__main__':
    earthquake = AllMapEarthquake(
        input_scenario_name='Earthquake migracion',
        output_scenario_name='Earthquake migracion_output'
    )
    earthquake.convert()
