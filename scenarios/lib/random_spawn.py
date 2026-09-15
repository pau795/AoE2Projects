from collections import Counter

from AoE2ScenarioParser.datasets.players import PlayerId
from AoE2ScenarioParser.datasets.trigger_lists import ObjectAttribute, Operation
from AoE2ScenarioParser.datasets.units import UnitInfo
from AoE2ScenarioParser.scenarios.aoe2_scenario import AoE2Scenario
from AoE2ScenarioParser.scenarios.support.data_triggers import DataTriggers

from scenarios.lib.equally_probable_trigger_list import FastEquallyProbableTriggerList


class RandomSpawn:
    def __init__(self, scenario: AoE2Scenario, data_triggers: DataTriggers, player_list: list, zone_relation: dict):
        self.scenario = scenario
        self.trigger_manager = scenario.trigger_manager
        self.data_triggers = data_triggers
        self.player_list = player_list
        self.zone_relation = zone_relation

        zone_dict = self._get_zone_dict()
        self._check_zone_dict_sanity(zone_dict)

        player_zone_dict = {}
        for player in self.player_list:
            player_zone_dict[player] = {}
            for zone in zone_dict:
                zone_triggers = []
                for resource in zone_dict[zone]:
                    resource_trigger_list = []
                    for number in zone_dict[zone][resource]:
                        create_object = self.trigger_manager.add_trigger(f"Create {zone} {resource} {number}", enabled=False)
                        for unit_list in zone_dict[zone][resource][number]:
                            for unit in unit_list:
                                create_object.new_effect.create_object(
                                    object_list_unit_id=unit.unit_const,
                                    location_x=int(unit.x),
                                    location_y=int(unit.y),
                                    source_player=PlayerId.GAIA if unit.player == PlayerId.GAIA else player
                                )
                                if "tc" == resource.lower():
                                    create_object.new_effect.change_view(
                                        location_x=int(unit.x),
                                        location_y=int(unit.y),
                                        source_player=player,
                                        scroll=False
                                    )

                        resource_trigger_list.append(create_object)
                    FastEquallyProbableTriggerList(self.trigger_manager, resource_trigger_list)
                    zone_triggers.extend(resource_trigger_list)
                player_zone_dict[player][zone] = zone_triggers
        for source_player, player_zones in self.zone_relation.items():
            zone_activation_triggers = []
            for source_zone, target_player_zones in player_zones.items():
                activation_triggers = self.trigger_manager.add_trigger(f"Activate P{source_player} {source_zone}", enabled=True, execute_on_load=False)
                for trigger in player_zone_dict[source_player][source_zone]:
                    activation_triggers.new_effect.activate_trigger(trigger.trigger_id)
                for target_player, target_zone in target_player_zones.items():
                    for trigger in player_zone_dict[target_player][target_zone]:
                        activation_triggers.new_effect.activate_trigger(trigger.trigger_id)
                zone_activation_triggers.append(activation_triggers)
            FastEquallyProbableTriggerList(self.trigger_manager, zone_activation_triggers)
        for key, unit_list in self.data_triggers.objects.items():
            if key.startswith("RS_"):
                for unit in unit_list:
                    self.scenario.unit_manager.remove_unit(unit.reference_id)
        # HORSE
        horse_vision = self.trigger_manager.add_trigger("Horse Vision", execute_on_load=True)
        delete_horses = self.trigger_manager.add_trigger("Remove Horses")
        for player in self.player_list:
            horse_vision.new_effect.modify_attribute(
                object_list_unit_id=UnitInfo.HORSE_A.ID,
                object_attributes=ObjectAttribute.LINE_OF_SIGHT,
                operation=Operation.SET,
                quantity=0,
                source_player=player
            )
            horse_vision.new_effect.modify_attribute(
                object_list_unit_id=UnitInfo.HORSE_A.ID,
                object_attributes=ObjectAttribute.SEARCH_RADIUS,
                operation=Operation.SET,
                quantity=0,
                source_player=player
            )

            delete_horses.new_condition.timer(2)
            delete_horses.new_effect.remove_object(
                source_player=player,
                object_list_unit_id=UnitInfo.HORSE_A.ID
            )

    def _get_zone_dict(self) -> dict:
        zone_dict = {}
        rs_keys = [x for x in self.data_triggers.objects.keys() if x.startswith("RS_")]

        for key in rs_keys:
            key_parts = key.split("_")
            if len(key_parts) != 4:
                raise ValueError(f"Invalid RS object key format: {key}")

            _, zone, resource, number = key_parts
            if zone not in zone_dict:
                zone_dict[zone] = {}
            if resource not in zone_dict[zone]:
                zone_dict[zone][resource] = {}
            if number not in zone_dict[zone][resource]:
                zone_dict[zone][resource][number] = []
            zone_dict[zone][resource][number].append(self.data_triggers.objects[key])

        return zone_dict

    @staticmethod
    def _check_zone_dict_sanity(zone_dict: dict) -> None:
        if not zone_dict:
            raise ValueError("No RS objects found in data_triggers.objects")

        errors = []
        zone_keys = {
            zone: {(resource, number) for resource, numbers in resources.items() for number in numbers}
            for zone, resources in zone_dict.items()
        }
        reference_zone = next(iter(zone_keys))
        reference_keys = zone_keys[reference_zone]

        for zone, keys in zone_keys.items():
            missing_keys = sorted(reference_keys - keys)
            extra_keys = sorted(keys - reference_keys)
            if missing_keys:
                errors.append(f"{zone} is missing resource/number keys: {missing_keys}")
            if extra_keys:
                errors.append(f"{zone} has extra resource/number keys: {extra_keys}")

        reference_id_keys = {}
        for zone, resources in zone_dict.items():
            for resource, numbers in resources.items():
                for number, unit_lists in numbers.items():
                    key = f"{zone}_{resource}_{number}"
                    for unit_list in unit_lists:
                        for unit in unit_list:
                            if unit.reference_id in reference_id_keys:
                                errors.append(
                                    f"reference_id {unit.reference_id} is repeated in "
                                    f"{reference_id_keys[unit.reference_id]} and {key}"
                                )
                            else:
                                reference_id_keys[unit.reference_id] = key

        for resource, number in sorted(reference_keys):
            signatures = {}
            for zone in zone_dict:
                if resource not in zone_dict[zone] or number not in zone_dict[zone][resource]:
                    continue

                unit_lists = zone_dict[zone][resource][number]
                unit_const_counter = Counter(
                    unit.unit_const
                    for unit_list in unit_lists
                    for unit in unit_list
                )
                signatures[zone] = (
                    len(unit_lists),
                    Counter(len(unit_list) for unit_list in unit_lists),
                    unit_const_counter,
                )

            first_signature = next(iter(signatures.values()))
            if all(signature == first_signature for signature in signatures.values()):
                continue

            reference_signature = signatures.get(reference_zone)
            for zone, signature in signatures.items():
                if zone == reference_zone or signature == reference_signature:
                    continue

                errors.append(
                    f"{zone}_{resource}_{number} does not match "
                    f"{reference_zone}_{resource}_{number}: "
                    f"{RandomSpawn._format_signature(signature)} != "
                    f"{RandomSpawn._format_signature(reference_signature)}"
                )

        if errors:
            raise ValueError("Invalid RS objects:\n" + "\n".join(f"- {error}" for error in errors))

    @staticmethod
    def _format_signature(signature: tuple) -> str:
        unit_list_count, unit_list_lengths_counter, unit_const_counter = signature
        return (
            f"{unit_list_count} unit lists, "
            f"lengths={dict(sorted(unit_list_lengths_counter.items()))}, "
            f"unit_consts={dict(sorted(unit_const_counter.items()))}"
        )



