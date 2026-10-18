import random

from AoE2ScenarioParser.datasets.players import PlayerId
from AoE2ScenarioParser.objects.support.tile import Tile

from scenarios.lib.civ_settings import CivSettings
from scenarios.lib.parser_project import ParserProject
from scenarios.lib.random_spawn import RandomSpawn
from scenarios.lib.thunder_factory import ThunderFactory
from scenarios.procesados.random.desert_madness.general.teleports import players


class ThunderDunes(ParserProject):
    RANDOM_SEED = 123156
    RAIN_SOUND = "light_rain"
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
        self.trigger_manager = self.scenario.trigger_manager
        self.data_triggers = self.scenario.actions.load_data_triggers()
        self.map_manager = self.scenario.map_manager
        self.unit_manager = self.scenario.unit_manager
        self.xs_manager = self.scenario.xs_manager
        self.player_list = [PlayerId.ONE, PlayerId.TWO]
        random.seed(self.RANDOM_SEED)

    def rain_sound(self, sound_tiles: list[Tile]):
        rain_trigger = self.trigger_manager.add_trigger('Rain Sound', looping=True)
        rain_trigger.new_condition.timer(150)
        for tile in sound_tiles:
            for player in self.player_list:
                rain_trigger.new_effect.play_sound(
                    sound_name=self.RAIN_SOUND,
                    location_x=tile.x,
                    location_y=tile.y,
                    source_player=player,
                )

    def process(self):
        RandomSpawn(self.scenario, self.data_triggers, self.player_list, self.RS_ZONE_RELATION)
        CivSettings(self.scenario, self.player_list, delay=2)
        thunder_factory = ThunderFactory(
            self.scenario,
            self.player_list,
            500,
            25,
            60
        )
        thunder_factory.set_thunder_flags()
        thunder_areas = self.data_triggers.areas['thunder_dunes']
        for i, area in enumerate(thunder_areas):
            thunder_factory.set_thunder_zone(area, i)
        thunder_factory.set_thunder_flag_damage()
        self.rain_sound([Tile(int(x.get_center()[0]), int(x.get_center()[1])) for x in thunder_areas])


if __name__ == '__main__':
    thunder_dunes_class = ThunderDunes(
        input_scenario_name='EDIT_THUNDER_DUNES_1V1',
        output_scenario_name='OUTPUT_THUNDER_DUNES_1V1'
    )
    thunder_dunes_class.convert()
