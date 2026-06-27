from AoE2ScenarioParser.objects.data_objects.trigger import Trigger
from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario


class RandomTrigger:
    def __init__(self, scenario: AoE2DEScenario, trigger: Trigger, probability: int):
        self.scenario = scenario
        self.trigger_manager = scenario.trigger_manager
        self.target_trigger = trigger
        self.probability = probability
        self.probability_enabler_trigger = self.trigger_manager.add_trigger(f'{self.target_trigger.name} Probability Enabler', enabled=False)
        self.probability_trigger = self.trigger_manager.add_trigger(f'{self.target_trigger.name} Probability {self.probability}', enabled=False)
        self.inverse_probability_trigger = self.trigger_manager.add_trigger(f'{self.target_trigger.name} Inverse Probability', enabled=False)
        self.probability_trigger.new_condition.chance(self.probability)
        self.probability_trigger.new_effect.activate_trigger(self.target_trigger.trigger_id)
        self.probability_trigger.new_effect.deactivate_trigger(self.inverse_probability_trigger.trigger_id)
        self.inverse_probability_trigger.new_effect.deactivate_trigger(self.probability_trigger.trigger_id)
        self.probability_enabler_trigger.new_effect.activate_trigger(self.probability_trigger.trigger_id)
        self.probability_enabler_trigger.new_effect.activate_trigger(self.inverse_probability_trigger.trigger_id)

