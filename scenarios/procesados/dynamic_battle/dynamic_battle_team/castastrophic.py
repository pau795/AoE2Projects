from AoE2ScenarioParser.datasets.players import PlayerId

from scenarios.lib.civ_settings import CivSettings
from scenarios.lib.earthquake_factory import EarthquakeFactory
from scenarios.lib.parser_project import ParserProject
from scenarios.lib.tsunami_factory import TsunamiFactory
from scenarios.lib.twister_factory import TwisterFactory
from scenarios.lib.vulkan_factory import VulkanFactory


class Catastrophic(ParserProject):

    def __init__(self, input_scenario_name: str, output_scenario_name: str):
        super().__init__(input_scenario_name, output_scenario_name)
        data_triggers = self.scenario.actions.load_data_triggers()
        self.earthquake_areas = data_triggers.areas['earthquake']
        self.twister_tiles = data_triggers.tiles['twister']
        self.tsunami_tiles = data_triggers.tiles['tsunami']
        self.player_list = [PlayerId.ONE, PlayerId.TWO, PlayerId.THREE, PlayerId.FOUR, PlayerId.FIVE, PlayerId.SIX, PlayerId.SEVEN, PlayerId.EIGHT]

    def process(self):
        CivSettings(self.scenario, self.player_list, nomad_players=[True, True, True, True, True, True, True, True])
        VulkanFactory(
            scenario=self.scenario,
            first_stage_time=600,
            second_stage_time=1200,
            explosion_period=130,
            lava_damage=30,
            volcan_sound="volcan",
            player_list=self.player_list
        )
        EarthquakeFactory(
            scenario=self.scenario,
            initial_delay=900,
            warning_delay=30,
            earthquake_duration=30,
            period_list=[420],
            damage=20,
            area_list=self.earthquake_areas,
            crack_sound='grietas',
            earthquake_sound='terremoto',
            player_list=self.player_list
        )
        twister_factory = TwisterFactory(
            scenario=self.scenario,
            twister_sound_name='twister',
            player_list=self.player_list,
            sound_delay=500,
        )
        twister_factory.twister_stats()
        twister_factory.twister_sound()
        for twister_center in self.twister_tiles:
            twister_factory.spawn_tornado(
                center=twister_center,
                radius=20,
                arms=10,
                drag_radius=12,
                inner_radius=7,
                spawn_times=[180],
                duration_times=[45]
            )
        tsunami_factory = TsunamiFactory(
            scenario=self.scenario,
            tsunami_sound_name='sirena60',
            tsunami_speed=2,
            tsunami_unit_damage=30,
            player_list=self.player_list
        )
        tsunami_factory.tsunami_stats()
        tsunami_factory.border_check(bottom_right=True)
        tsunami_factory.config_tsunami(
            tile_list=self.tsunami_tiles,
            amplitude=8,
            thickness=1.2,
            wave_delay=15,
            tsunami_periods=[660],
            display_sound=True
        )


if __name__ == '__main__':
    catastrophic_class = Catastrophic(
        input_scenario_name='EDIT_CATASTROPHIC_4V4',
        output_scenario_name='OUTPUT_CATASTROPHIC_4V4'
    )
    catastrophic_class.convert()
