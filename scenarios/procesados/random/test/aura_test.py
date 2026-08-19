from AoE2ScenarioParser.datasets.players import PlayerId
from AoE2ScenarioParser.datasets.trigger_lists import ObjectAttribute, Operation, CombatAbility
from AoE2ScenarioParser.datasets.units import UnitInfo

from scenarios.lib.parser_project import ParserProject
from scenarios.lib.unit_modifier import UnitModifier
from scenarios.lib.xs.unit_tasks import AuraTask, TaskTargets, AuraFlags, TargetOwnership
from scenarios.lib.xs.xs_constants import XsConstantObjectClass, XsConstantAttribute, XsConstantEffectAmount


class Test1(ParserProject):

    def __init__(self, input_scenario_name: str, output_scenario_name: str):
        super().__init__(input_scenario_name, output_scenario_name)
        self.trigger_manager = self.scenario.trigger_manager
        self.map_manager = self.scenario.map_manager
        self.unit_manager = self.scenario.unit_manager
        self.xs_manager = self.scenario.xs_manager
        self.xs_manager.initialise_xs_trigger()

    def process(self):
        (UnitModifier(self.scenario, UnitInfo.ARCHER.ID, PlayerId.ONE)
         .modify_attribute(ObjectAttribute.COMBAT_ABILITY, Operation.ADD, CombatAbility.ENABLE_AURA_ABILITY)
         .add_task(AuraTask(
            affected_objects=TaskTargets(True, (XsConstantObjectClass.ARCHER_CLASS, XsConstantObjectClass.CAVALRY_CLASS)),
            effect_range=5,
            modifier_value=-100,
            minimum_units_in_range=1,
            modified_attribute=XsConstantEffectAmount.REGENERATION_RATE,
            flags=AuraTask.Flags.ADD | AuraTask.Flags.CIRCULAR | AuraFlags.VISIBLE_RANGE,
            target_ownership=AuraTask.Ownership.ALL
         ))
         ).create_triggers()
        (UnitModifier(self.scenario, UnitInfo.ARAMBAI.ID, PlayerId.ONE)
         .modify_attribute(ObjectAttribute.COMBAT_ABILITY, Operation.ADD, CombatAbility.ENABLE_AURA_ABILITY)
         .add_task(AuraTask(
            affected_objects=TaskTargets(True, (XsConstantObjectClass.ARCHER_CLASS, XsConstantObjectClass.CAVALRY_CLASS)),
            effect_range=5,
            modifier_value=-100,
            minimum_units_in_range=1,   
            modified_attribute=XsConstantEffectAmount.REGENERATION_RATE,
            flags=AuraTask.Flags.ADD | AuraTask.Flags.CIRCULAR | AuraFlags.VISIBLE_RANGE,
            target_ownership=AuraTask.Ownership.ALL
         ))
         ).create_triggers()

        pass


if __name__ == '__main__':
    test1 = Test1(
        input_scenario_name=f'task_test',
        output_scenario_name=f'task_test_output'
    )
    test1.convert()
