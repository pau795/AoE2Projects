from AoE2ScenarioParser.datasets.players import PlayerId
from AoE2ScenarioParser.datasets.trigger_lists import ObjectAttribute, Operation, FogVisibility, DamageClass, \
    AttackStance, ActionType
from AoE2ScenarioParser.datasets.units import UnitInfo
from AoE2ScenarioParser.objects.managers.trigger_manager import TriggerManager
from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario
from AoE2ScenarioParser.scenarios.support.data_triggers import DataTriggers


class SteppeLancers:

    def __init__(self, scenario: AoE2DEScenario, trigger_data: DataTriggers):
        self.trigger_manager: TriggerManager = scenario.trigger_manager
        self.trigger_data = trigger_data
        self.steppe_lancers_units = self.trigger_data.objects['steppe_lancers']
        self.steppe_lancers_target = self.trigger_data.tiles['steppe_lancers_target']
        self.steppe_lancers()

    def steppe_lancers(self):
        steppe_lancers_attributes = self.trigger_manager.add_trigger("Steppe Lancers Attributes")
        steppe_lancers_attributes.new_effect.modify_attribute(
            object_list_unit_id=UnitInfo.STEPPE_LANCER.ID,
            source_player=PlayerId.EIGHT,
            object_attributes=ObjectAttribute.HIT_POINTS,
            operation=Operation.SET,
            quantity=1000
        )
        steppe_lancers_attributes.new_effect.modify_attribute(
            object_list_unit_id=UnitInfo.STEPPE_LANCER.ID,
            source_player=PlayerId.EIGHT,
            object_attributes=ObjectAttribute.ATTACK,
            operation=Operation.SET,
            armour_attack_class=DamageClass.BASE_MELEE,
            armour_attack_quantity=25
        )
        steppe_lancers_attributes.new_effect.modify_attribute(
            object_list_unit_id=UnitInfo.STEPPE_LANCER.ID,
            source_player=PlayerId.EIGHT,
            object_attributes=ObjectAttribute.SHOWN_ATTACK,
            operation=Operation.SET,
            quantity=25
        )
        steppe_lancers_attributes.new_effect.modify_attribute(
            object_list_unit_id=UnitInfo.STEPPE_LANCER.ID,
            source_player=PlayerId.EIGHT,
            object_attributes=ObjectAttribute.MOVEMENT_SPEED,
            operation=Operation.SET,
            quantity=5
        )
        steppe_lancers_attributes.new_effect.modify_attribute(
            object_list_unit_id=UnitInfo.STEPPE_LANCER.ID,
            source_player=PlayerId.EIGHT,
            object_attributes=ObjectAttribute.MOVEMENT_SPEED,
            operation=Operation.DIVIDE,
            quantity=2
        )
        steppe_lancers_attributes.new_effect.modify_attribute(
            object_list_unit_id=UnitInfo.STEPPE_LANCER.ID,
            source_player=PlayerId.EIGHT,
            object_attributes=ObjectAttribute.MAX_RANGE,
            operation=Operation.SET,
            quantity=1
        )
        steppe_lancers_attributes.new_effect.modify_attribute(
            object_list_unit_id=UnitInfo.STEPPE_LANCER.ID,
            source_player=PlayerId.EIGHT,
            object_attributes=ObjectAttribute.MAX_RANGE,
            operation=Operation.DIVIDE,
            quantity=2
        )
        steppe_lancers_attributes.new_effect.modify_attribute(
            object_list_unit_id=UnitInfo.STEPPE_LANCER.ID,
            source_player=PlayerId.EIGHT,
            object_attributes=ObjectAttribute.SHOWN_RANGE,
            operation=Operation.SET,
            quantity=1
        )
        steppe_lancers_attributes.new_effect.modify_attribute(
            object_list_unit_id=UnitInfo.STEPPE_LANCER.ID,
            source_player=PlayerId.EIGHT,
            object_attributes=ObjectAttribute.SHOWN_RANGE,
            operation=Operation.DIVIDE,
            quantity=2
        )
        steppe_lancers_attributes.new_effect.modify_attribute(
            object_list_unit_id=UnitInfo.STEPPE_LANCER.ID,
            source_player=PlayerId.EIGHT,
            object_attributes=ObjectAttribute.FOG_VISIBILITY,
            operation=Operation.SET,
            quantity=FogVisibility.ALWAYS_VISIBLE
        )
        for unit in self.steppe_lancers_units:
            steppe_lancers_attributes.new_effect.change_object_stance(
                selected_object_ids=unit.reference_id,
                source_player=PlayerId.EIGHT,
                attack_stance=AttackStance.STAND_GROUND
            )
            steppe_lancers_attributes.new_effect.disable_unit_targeting(
                selected_object_ids=unit.reference_id,
                source_player=PlayerId.EIGHT
            )
        for unit, target in zip(self.steppe_lancers_units, self.steppe_lancers_target):
            steppe_lancers_attributes.new_effect.task_object(
                selected_object_ids=unit.reference_id,
                source_player=PlayerId.EIGHT,
                location_x=target.x,
                location_y=target.y,
                action_type=ActionType.PATROL
            )






