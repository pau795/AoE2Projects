from AoE2ScenarioParser.datasets.other import OtherInfo
from AoE2ScenarioParser.datasets.players import PlayerId
from AoE2ScenarioParser.datasets.trigger_lists import ObjectAttribute, Operation

from scenarios.lib.parser_project import ParserProject
from scenarios.lib.civ_settings import CivSettings
from scenarios.lib.tsunami_factory import TsunamiFactory


class TsunamiMultiplayer(ParserProject):

    def __init__(self, input_scenario_name: str, output_scenario_name: str):
        super().__init__(input_scenario_name, output_scenario_name)
        data_triggers = self.scenario.actions.load_data_triggers()
        self.tsunami1_tiles = data_triggers.tiles['tsunami_1']
        self.tsunami2_tiles = data_triggers.tiles['tsunami_2']
        self.player_list = [PlayerId.ONE, PlayerId.TWO, PlayerId.THREE, PlayerId.FOUR, PlayerId.FIVE, PlayerId.SIX]
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
        tsunami_factory.border_check(bottom_right=True, bottom_left=True)
        tsunami_factory.config_tsunami(
            tile_list=self.tsunami1_tiles,
            amplitude=8,
            thickness=1.2,
            wave_delay=15,
            tsunami_periods=[600],
            display_sound=True
        )
        tsunami_factory.config_tsunami(
            tile_list=self.tsunami2_tiles,
            amplitude=8,
            thickness=1.2,
            wave_delay=15,
            tsunami_periods=[600],
            display_sound=False
        )
        CivSettings(self.scenario, self.player_list)
        self.trees()

    def trees(self):
        tree_trigger = self.trigger_manager.add_trigger("Initial Trees")
        tree_trigger.new_effect.modify_attribute(
            object_list_unit_id=OtherInfo.TREE_OAK_AUTUMN_SNOW.ID,
            source_player=PlayerId.GAIA,
            object_attributes=ObjectAttribute.AMOUNT_OF_1ST_RESOURCE_STORAGE,
            operation=Operation.SET,
            quantity=250
        )

        replace_trees = self.trigger_manager.add_trigger("Replace Trees")
        replace_trees.new_effect.replace_object(
            object_list_unit_id=OtherInfo.TREE_OAK_AUTUMN_SNOW.ID,
            source_player=PlayerId.GAIA,
            target_player=PlayerId.GAIA,
            object_list_unit_id_2=OtherInfo.FLAG_A.ID
        )

        replace_trees.new_effect.replace_object(
            object_list_unit_id=OtherInfo.FLAG_A.ID,
            source_player=PlayerId.GAIA,
            target_player=PlayerId.GAIA,
            object_list_unit_id_2=OtherInfo.TREE_OAK_AUTUMN_SNOW.ID
        )


if __name__ == '__main__':
    tsunami_class = TsunamiMultiplayer(
        input_scenario_name='EDIT_TSUNAMI_3V3',
        output_scenario_name='OUTPUT_TSUNAMI_3V3'
    )
    tsunami_class.convert()
