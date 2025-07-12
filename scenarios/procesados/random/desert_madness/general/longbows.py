from AoE2ScenarioParser.datasets.players import PlayerId
from AoE2ScenarioParser.datasets.projectiles import ProjectileInfo
from AoE2ScenarioParser.datasets.trigger_lists import ObjectAttribute, Operation, FogVisibility, DamageClass, \
    AttackStance, ActionType, CombatAbility
from AoE2ScenarioParser.datasets.units import UnitInfo
from AoE2ScenarioParser.objects.managers.trigger_manager import TriggerManager
from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario
from AoE2ScenarioParser.scenarios.support.data_triggers import DataTriggers


class Longbows:

    def __init__(self, scenario: AoE2DEScenario, trigger_data: DataTriggers):
        self.trigger_manager: TriggerManager = scenario.trigger_manager
        self.trigger_data = trigger_data
        self.longbows = self.trigger_data.objects['longbows']
        self.longbows_target = self.trigger_data.tiles['longbows_target']
        self.longbows_triggers()

    def longbows_triggers(self):
        longbows_attributes = self.trigger_manager.add_trigger("Longbows Attributes")

        longbows_attributes.new_effect.modify_attribute(
            object_list_unit_id=UnitInfo.LONGBOWMAN.ID,
            source_player=PlayerId.EIGHT,
            object_attributes=ObjectAttribute.HIT_POINTS,
            operation=Operation.SET,
            quantity=1000
        )
        longbows_attributes.new_effect.modify_attribute(
            object_list_unit_id=UnitInfo.LONGBOWMAN.ID,
            source_player=PlayerId.EIGHT,
            object_attributes=ObjectAttribute.COMBAT_ABILITY,
            operation=Operation.SET,
            quantity=CombatAbility.ATTACK_GROUND
        )
        longbows_attributes.new_effect.modify_attribute(
            object_list_unit_id=UnitInfo.LONGBOWMAN.ID,
            source_player=PlayerId.EIGHT,
            object_attributes=ObjectAttribute.ATTACK,
            operation=Operation.SET,
            armour_attack_class=DamageClass.BASE_PIERCE,
            armour_attack_quantity=25
        )
        longbows_attributes.new_effect.modify_attribute(
            object_list_unit_id=UnitInfo.LONGBOWMAN.ID,
            source_player=PlayerId.EIGHT,
            object_attributes=ObjectAttribute.SHOWN_ATTACK,
            operation=Operation.SET,
            quantity=25
        )
        longbows_attributes.new_effect.modify_attribute(
            object_list_unit_id=UnitInfo.LONGBOWMAN.ID,
            source_player=PlayerId.EIGHT,
            object_attributes=ObjectAttribute.ACCURACY_PERCENT,
            operation=Operation.SET,
            quantity=100
        )
        longbows_attributes.new_effect.modify_attribute(
            object_list_unit_id=UnitInfo.LONGBOWMAN.ID,
            source_player=PlayerId.EIGHT,
            object_attributes=ObjectAttribute.MAX_RANGE,
            operation=Operation.SET,
            quantity=10
        )
        longbows_attributes.new_effect.modify_attribute(
            object_list_unit_id=UnitInfo.LONGBOWMAN.ID,
            source_player=PlayerId.EIGHT,
            object_attributes=ObjectAttribute.SHOWN_RANGE,
            operation=Operation.SET,
            quantity=10
        )
        longbows_attributes.new_effect.modify_attribute(
            object_list_unit_id=UnitInfo.LONGBOWMAN.ID,
            source_player=PlayerId.EIGHT,
            object_attributes=ObjectAttribute.FOG_VISIBILITY,
            operation=Operation.SET,
            quantity=FogVisibility.ALWAYS_VISIBLE
        )
        longbows_attributes.new_effect.modify_attribute(
            object_list_unit_id=UnitInfo.LONGBOWMAN.ID,
            source_player=PlayerId.EIGHT,
            object_attributes=ObjectAttribute.PROJECTILE_UNIT,
            operation=Operation.SET,
            quantity=ProjectileInfo.WAR_GALLEY_FIRE.ID)
        for unit in self.longbows:
            longbows_attributes.new_effect.change_object_stance(
                selected_object_ids=unit.reference_id,
                source_player=PlayerId.EIGHT,
                attack_stance=AttackStance.NO_ATTACK_STANCE
            )
            longbows_attributes.new_effect.disable_unit_targeting(
                selected_object_ids=unit.reference_id,
                source_player=PlayerId.EIGHT
            )
        for unit, target in zip(self.longbows, self.longbows_target):
            longbows_attributes.new_effect.task_object(
                selected_object_ids=unit.reference_id,
                source_player=PlayerId.EIGHT,
                location_x=target.x,
                location_y=target.y,
                action_type=ActionType.ATTACK_GROUND
            )






