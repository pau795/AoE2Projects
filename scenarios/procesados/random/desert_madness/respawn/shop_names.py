from AoE2ScenarioParser.datasets.players import PlayerId
from AoE2ScenarioParser.objects.managers.trigger_manager import TriggerManager
from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario
from AoE2ScenarioParser.scenarios.support.data_triggers import DataTriggers


class ShopNames:

    def __init__(self, scenario: AoE2DEScenario, trigger_data: DataTriggers):
        self.trigger_manager: TriggerManager = scenario.trigger_manager
        self.trigger_data = trigger_data
        self.shop_names()

    def shop_names(self):
        shop_names = self.trigger_data.objects['shop_names']
        shop_names_trigger = self.trigger_manager.add_trigger("Shop Names")

        shop_names_trigger.new_effect.change_object_name(
            selected_object_ids=shop_names[0].reference_id,
            source_player=PlayerId.EIGHT,
            message="Upgrade Lumberjacks")

        shop_names_trigger.new_effect.change_object_name(
            selected_object_ids=shop_names[1].reference_id,
            source_player=PlayerId.EIGHT,
            message="Upgrade Gold Miners")

        shop_names_trigger.new_effect.change_object_name(
            selected_object_ids=shop_names[2].reference_id,
            source_player=PlayerId.EIGHT,
            message="Upgrade Stone Miners")

        shop_names_trigger.new_effect.change_object_name(
            selected_object_ids=shop_names[3].reference_id,
            source_player=PlayerId.EIGHT,
            message="Upgrade Villagers")

        shop_names_trigger.new_effect.change_object_name(
            selected_object_ids=shop_names[4].reference_id,
            source_player=PlayerId.EIGHT,
            message="Upgrade Builders and Repairers")

        shop_names_trigger.new_effect.change_object_name(
            selected_object_ids=shop_names[5].reference_id,
            source_player=PlayerId.EIGHT,
            message="Upgrade Foragers")

        shop_names_trigger.new_effect.change_object_name(
            selected_object_ids=shop_names[6].reference_id,
            source_player=PlayerId.EIGHT,
            message="Upgrade Fishermen")

        shop_names_trigger.new_effect.change_object_name(
            selected_object_ids=shop_names[7].reference_id,
            source_player=PlayerId.EIGHT,
            message="Upgrade Hunters")