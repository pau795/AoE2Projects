from AoE2ScenarioParser.datasets.players import PlayerId

from scenarios.lib.earthquake_factory import EarthquakeFactory
from scenarios.lib.nomad_start import NomadStart
from scenarios.lib.parser_project import ParserProject
from scenarios.lib.civ_settings import CivSettings


class AllMapEarthquake(ParserProject):

    def __init__(self, input_scenario_name: str, output_scenario_name: str):
        super().__init__(input_scenario_name, output_scenario_name)

    def process(self):
        data_triggers = self.scenario.actions.load_data_triggers()
        earthquake_areas = data_triggers.areas['earthquake 2']
        players = [PlayerId.ONE, PlayerId.TWO]
        EarthquakeFactory(
            scenario=self.scenario,
            initial_delay=900,
            warning_delay=30,
            earthquake_duration=30,
            period_list=[240, 270, 300, 330, 360, 390, 420],
            damage=30,
            area_list=earthquake_areas,
            crack_sound='grietas',
            earthquake_sound='terremoto',
            player_list=players
        )
        NomadStart(self.scenario.trigger_manager, data_triggers, players)
        CivSettings(self.scenario, players)


earthquake = AllMapEarthquake(
    input_scenario_name='EARTHQUAKE nomad 1vs1',
    output_scenario_name='EARTHQUAKE nomad 1vs1_output'
)
earthquake.convert()
