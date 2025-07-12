from typing import Self

from AoE2ScenarioParser.datasets.trigger_lists import ObjectAttribute
from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario


class UnitModifier:
    def __init__(self, scenario: AoE2DEScenario, unit_id: int, source_player: int):
        self._unit_id = unit_id
        self._source_player = source_player
        self._modify_unit_trigger = scenario.trigger_manager.add_trigger(f"P{source_player} Modify Unit {unit_id}")
        self._attribute_list: list[tuple[int, int, int, int]] = []

    def modify_attribute(self, attribute: int, operation: int, quantity: int, armor_attack_class: int = None) -> Self:
        self._attribute_list.append((attribute, operation, quantity, armor_attack_class))
        return self

    def create_triggers(self) -> None:
        for object_attribute, operation, quantity, attack_armor_class in self._attribute_list:
            is_attack_or_armor = object_attribute in [ObjectAttribute.ATTACK, ObjectAttribute.ARMOR]
            self._modify_unit_trigger.new_effect.modify_attribute(
                object_list_unit_id=self._unit_id,
                source_player=self._source_player,
                object_attributes=object_attribute,
                operation=operation,
                quantity=None if is_attack_or_armor else quantity,
                armour_attack_quantity=quantity if is_attack_or_armor else None,
                armour_attack_class=attack_armor_class
            )
