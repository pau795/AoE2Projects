from AoE2ScenarioParser.datasets.players import PlayerId
from AoE2ScenarioParser.objects.managers.trigger_manager import TriggerManager


class EqualRandomProbability:
    def __init__(self, trigger_manager, target_trigger_list, trigger_name):
        self.trigger_manager: TriggerManager = trigger_manager
        self.target_trigger_list = target_trigger_list
        self.trigger_name = trigger_name
        self.probability_trigger_list = []
        self.enable_probability_trigger = self.trigger_manager.add_trigger("Enable Random Probability", enabled=False)
        self.__create_probability_triggers()

    def __create_probability_triggers(self):
        for i, trigger in enumerate(self.target_trigger_list):
            probability_trigger = self.trigger_manager.add_trigger(
                f"Random Probability {self.trigger_name} {i}", enabled=False
            )
            chance = round(1 / (len(self.target_trigger_list) - i) * 100)
            probability_trigger.new_condition.chance(chance)
            probability_trigger.new_effect.activate_trigger(trigger_id=trigger.trigger_id)
            self.probability_trigger_list.append(probability_trigger)

        for trigger_a in self.probability_trigger_list:
            for trigger_b in self.probability_trigger_list:
                trigger_a.new_effect.deactivate_trigger(trigger_id=trigger_b.trigger_id)

        for trigger in self.probability_trigger_list:
            self.enable_probability_trigger.new_effect.activate_trigger(trigger_id=trigger.trigger_id)
