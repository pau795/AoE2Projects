from AoE2ScenarioParser.datasets.players import PlayerId

from scenarios.lib.earthquake_factory import EarthquakeFactory
from scenarios.lib.nomad_start import NomadStart
from scenarios.lib.parser_project import ParserProject
from scenarios.lib.civ_settings import CivSettings


class EarthquakeMultiplayer(ParserProject):

    def __init__(self,input_scenario_name: str, output_scenario_name: str):
        super().__init__(input_scenario_name, output_scenario_name)

    def process(self):
        data_triggers = self.scenario.actions.load_data_triggers()
        earthquake_areas = data_triggers.areas['earthquake 2']
        players = [PlayerId.ONE, PlayerId.TWO, PlayerId.THREE, PlayerId.FOUR, PlayerId.FIVE, PlayerId.SIX, PlayerId.SEVEN, PlayerId.EIGHT]
        CivSettings(self.scenario, players, nomad_players=[True, True, True, True, True, True, True, True])
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


if __name__ == '__main__':
    earthquake_class = EarthquakeMultiplayer(
        input_scenario_name=f'EDIT_EARTHQUAKE_4V4',
        output_scenario_name=f'OUTPUT_EARTHQUAKE_4V4'
    )
    earthquake_class.convert()
