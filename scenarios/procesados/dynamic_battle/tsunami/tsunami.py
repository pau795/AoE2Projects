from AoE2ScenarioParser.datasets.other import OtherInfo
from AoE2ScenarioParser.datasets.players import PlayerId
from AoE2ScenarioParser.datasets.trigger_lists import ObjectAttribute, Operation

from scenarios.lib.parser_project import ParserProject
from scenarios.lib.civ_settings import CivSettings
from scenarios.lib.tsunami_factory import TsunamiFactory


class Tsunami(ParserProject):

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
        tsunami_factory.border_check(bottom_right=True)
        tsunami_factory.config_tsunami(
            tile_list=self.tsunami_tiles,
            amplitude=8,
            thickness=1.2,
            wave_delay=15,
            tsunami_periods=[600]
        )
        CivSettings(self.scenario, self.player_list)
        self.trees()

    def trees(self):
        tree_trigger = self.trigger_manager.add_trigger("Initial Trees")
        tree_trigger.new_effect.modify_attribute(
            object_list_unit_id=OtherInfo.TREE_BIRCH.ID,
            source_player=PlayerId.GAIA,
            object_attributes=ObjectAttribute.AMOUNT_OF_1ST_RESOURCE_STORAGE,
            operation=Operation.SET,
            quantity=250
        )

        tree_trigger.new_effect.modify_attribute(
            object_list_unit_id=OtherInfo.TREE_PALM_FOREST.ID,
            source_player=PlayerId.GAIA,
            object_attributes=ObjectAttribute.AMOUNT_OF_1ST_RESOURCE_STORAGE,
            operation=Operation.SET,
            quantity=250
        )

        replace_trees = self.trigger_manager.add_trigger("Replace Trees")
        replace_trees.new_effect.replace_object(
            object_list_unit_id=OtherInfo.TREE_BIRCH.ID,
            source_player=PlayerId.GAIA,
            target_player=PlayerId.GAIA,
            object_list_unit_id_2=OtherInfo.FLAG_A.ID
        )

        replace_trees.new_effect.replace_object(
            object_list_unit_id=OtherInfo.FLAG_A.ID,
            source_player=PlayerId.GAIA,
            target_player=PlayerId.GAIA,
            object_list_unit_id_2=OtherInfo.TREE_BIRCH.ID
        )

        replace_trees.new_effect.replace_object(
            object_list_unit_id=OtherInfo.TREE_PALM_FOREST.ID,
            source_player=PlayerId.GAIA,
            target_player=PlayerId.GAIA,
            object_list_unit_id_2=OtherInfo.FLAG_B.ID
        )

        replace_trees.new_effect.replace_object(
            object_list_unit_id=OtherInfo.FLAG_B.ID,
            source_player=PlayerId.GAIA,
            target_player=PlayerId.GAIA,
            object_list_unit_id_2=OtherInfo.TREE_PALM_FOREST.ID
        )


if __name__ == '__main__':
    tsunami = Tsunami(
        input_scenario_name='EDIT_TSUNAMI_1V1',
        output_scenario_name='OUTPUT_TSUNAMI_1V1',
    )
    tsunami.convert()
