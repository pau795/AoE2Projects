import unittest
from dataclasses import fields

from AoE2ScenarioParser.datasets.trigger_lists import ObjectAttribute

from scenarios.lib.unit_modifier import UnitModifier
from scenarios.lib.xs import xs_constants
from scenarios.lib.xs.unit_tasks import (
    AdditionalSpawnTask,
    AmphibiousTask,
    AuraFlags,
    AuraTask,
    BuildTask,
    ConvertTask,
    DepositUnitTask,
    FlyTask,
    GarrisonTask,
    GenerateResourcesTask,
    HealTask,
    HPDamageModifierTask,
    HPTransformationTask,
    LootTask,
    MovementDamageTask,
    PickupUnitTask,
    RepairTask,
    StingerTask,
    TaskTargets,
    UnitRefundTask,
    XsConstant,
)
from scenarios.lib.xs.xs_constants import XsConstantAttribute, XsConstantColor, XsConstantTaskAttribute, XsConstantTaskType


class _FakeNewEffect:
    def __init__(self) -> None:
        self.modify_attribute_calls = []
        self.script_call_calls = []

    def modify_attribute(self, **kwargs):
        self.modify_attribute_calls.append(kwargs)

    def script_call(self, **kwargs):
        self.script_call_calls.append(kwargs)


class _FakeTrigger:
    def __init__(self, trigger_id: int, name: str) -> None:
        self.trigger_id = trigger_id
        self.name = name
        self.new_effect = _FakeNewEffect()


class _FakeTriggerManager:
    def __init__(self) -> None:
        self.triggers = []

    def add_trigger(self, name: str):
        trigger = _FakeTrigger(len(self.triggers), name)
        self.triggers.append(trigger)
        return trigger


class _FakeXsManager:
    def __init__(self) -> None:
        self.scripts = []

    def add_script(self, **kwargs):
        self.scripts.append(kwargs)


class _FakeScenario:
    def __init__(self) -> None:
        self.trigger_manager = _FakeTriggerManager()
        self.xs_manager = _FakeXsManager()


class UnitTaskTests(unittest.TestCase):
    def test_generated_xs_constant_categories_preserve_names_values_and_types(self) -> None:
        category_names = [
            name for name in xs_constants.__all__
            if name not in {"XsConstant", "XsConstantValue"}
        ]
        constant_count = sum(
            isinstance(value, XsConstant)
            for category_name in category_names
            for value in vars(getattr(xs_constants, category_name)).values()
        )

        self.assertEqual(21, len(category_names))
        self.assertEqual(878, constant_count)
        self.assertEqual("cAttributeFood", XsConstantAttribute.FOOD)
        self.assertEqual(0, XsConstantAttribute.FOOD.value)
        self.assertEqual("int", XsConstantAttribute.FOOD.xs_type)
        self.assertEqual("cTaskAttrWorkValue1", XsConstantTaskAttribute.WORK_VALUE_1)
        self.assertEqual(0, XsConstantTaskAttribute.WORK_VALUE_1.value)
        self.assertEqual("cTaskTypeMovementDamage", XsConstantTaskType.MOVEMENT_DAMAGE)
        self.assertEqual(152, XsConstantTaskType.MOVEMENT_DAMAGE.value)
        self.assertEqual("<BLUE>", XsConstantColor.BLUE.value)
        self.assertEqual("string", XsConstantColor.BLUE.xs_type)

    def test_task_class_docstrings_document_every_constructor_field(self) -> None:
        task_classes = [
            GarrisonTask,
            FlyTask,
            BuildTask,
            ConvertTask,
            HealTask,
            RepairTask,
            PickupUnitTask,
            DepositUnitTask,
            GenerateResourcesTask,
            MovementDamageTask,
            LootTask,
            AuraTask,
            AdditionalSpawnTask,
            StingerTask,
            HPTransformationTask,
            AmphibiousTask,
            HPDamageModifierTask,
            UnitRefundTask,
        ]

        for task_class in task_classes:
            with self.subTest(task_class=task_class.__name__):
                docstring = task_class.__doc__ or ""
                self.assertIn("Args:", docstring)
                for task_field in fields(task_class):
                    self.assertIn(f"{task_field.name}:", docstring)

    def test_all_requested_task_types_use_the_documented_xs_constants(self) -> None:
        tasks = [
            GarrisonTask(),
            FlyTask(),
            BuildTask(),
            ConvertTask(),
            HealTask(),
            RepairTask(),
            PickupUnitTask(transformed_unit_id=1),
            DepositUnitTask(transformed_unit_id=1),
            GenerateResourcesTask(resource_amount=1, output_resource=0, productivity_resource=600),
            MovementDamageTask(damage_per_tick=2.5, tick_interval_seconds=0.5, effect_range=0.75),
            LootTask(),
            AuraTask(modifier_value=1, effect_range=2, modified_attribute=9),
            AdditionalSpawnTask(spawned_unit_id=93, spawn_count=2),
            StingerTask(modifier_value=-0.8, effect_duration_seconds=5, modified_attribute=5),
            HPTransformationTask(transformed_unit_id=692, hp_threshold=-0.4),
            AmphibiousTask(terrain_or_terrain_type=1),
            HPDamageModifierTask(modifier_value=2, hp_percentage_threshold=0.2, modified_attribute=9),
            UnitRefundTask(refund_value=10, refunded_resource=3),
        ]
        expected_constants = [
            "cTaskTypeGarrison",
            "cTaskTypeFly",
            "cTaskTypeBuild",
            "cTaskTypeConvert",
            "cTaskTypeHeal",
            "cTaskTypeRepair",
            "cTaskTypePickupUnit",
            "cTaskTypeDepositUnit",
            "cTaskTypeGenerateResources",
            "cTaskTypeMovementDamage",
            "cTaskTypeLoot",
            "cTaskTypeAura",
            "cTaskTypeExtraSpawn",
            "cTaskTypeStinger",
            "cTaskTypeHPTransform",
            "cTaskTypeAmphibious",
            "cTaskTypeHPModifier",
            "cTaskTypeRefund",
        ]

        self.assertEqual(18, len(tasks))
        for task, expected_constant in zip(tasks, expected_constants):
            self.assertIn(
                f"xsTaskAmount(cTaskAttrTaskType, {expected_constant});",
                task.xs_setup_lines(),
            )

    def test_optional_fields_default_to_minus_one_and_unknown_fields_are_hidden(self) -> None:
        build_lines = BuildTask().xs_setup_lines()

        self.assertIn("xsTaskAmount(cTaskAttrWorkValue1, -1);", build_lines)
        self.assertIn("xsTaskAmount(cTaskAttrDepositSound, -1);", build_lines)
        self.assertFalse(any("cTaskAttrAutoSearch" in line for line in build_lines))
        self.assertFalse(any("cTaskAttrBuildingPick" in line for line in build_lines))
        self.assertFalse(any("cTaskAttrSearchWaitTime" in line for line in build_lines))

    def test_xs_constants_and_combined_flags_are_serialized_safely(self) -> None:
        task = AuraTask(
            modifier_value=5,
            effect_range=10.0,
            modified_attribute=XsConstant("cAttack"),
            flags=AuraFlags.CIRCULAR | AuraFlags.VISIBLE_RANGE,
        )

        lines = task.xs_setup_lines()
        self.assertIn("xsTaskAmount(cTaskAttrSearchWaitTime, cAttack);", lines)
        self.assertIn("xsTaskAmount(cTaskAttrCombatLevelFlag, 6);", lines)

        with self.assertRaises(ValueError):
            XsConstant("cAttack); xsChatData(\"bad\")")
        with self.assertRaises(TypeError):
            AuraTask(modifier_value="not-xs", effect_range=10, modified_attribute=9)

    def test_target_model_enforces_one_target_kind(self) -> None:
        with self.assertRaises(ValueError):
            TaskTargets.object_ids([])
        with self.assertRaises(ValueError):
            TaskTargets(None, [1])

        object_targets = TaskTargets.object_ids([4])
        class_targets = TaskTargets.object_classes([XsConstant("cInfantryClass")])

        self.assertEqual(
            [
                "xsTaskAmount(cTaskAttrObjectId, 4);",
                "xsTaskAmount(cTaskAttrObjectClass, -1);",
            ],
            object_targets.xs_lines_for_target(0),
        )
        self.assertEqual(
            [
                "xsTaskAmount(cTaskAttrObjectId, -1);",
                "xsTaskAmount(cTaskAttrObjectClass, cInfantryClass);",
            ],
            class_targets.xs_lines_for_target(0),
        )


class UnitModifierTaskTests(unittest.TestCase):
    def test_builder_generates_add_edit_remove_xs_and_script_call(self) -> None:
        scenario = _FakeScenario()
        targets = TaskTargets.object_classes(
            [XsConstant("cInfantryClass"), XsConstant("cArcherClass")]
        )
        aura = AuraTask(
            modifier_value=5,
            effect_range=10,
            modified_attribute=XsConstant("cAttack"),
            affected_objects=targets,
        )
        refund = UnitRefundTask(refund_value=10, refunded_resource=XsConstant("cAttributeGold"))

        modifier = UnitModifier(scenario, unit_id=629, source_player=1)
        result = (
            modifier
            .add_task(aura)
            .edit_task(refund, task_indices=7)
            .remove_tasks([2, 5])
            .create_triggers()
        )

        self.assertIs(modifier, result)
        self.assertEqual(1, len(scenario.xs_manager.scripts))
        script = scenario.xs_manager.scripts[0]["xs_string"]

        self.assertTrue(script.startswith("void unit_modifier_tasks_0()"))
        self.assertEqual(2, script.count("xsGetObjectTaskCount(629, 1)"))
        self.assertIn("xsTaskAmount(cTaskAttrObjectClass, cInfantryClass);", script)
        self.assertIn("xsTaskAmount(cTaskAttrObjectClass, cArcherClass);", script)
        self.assertIn("xsModifyObjectTasks(629, 1, 7, true);", script)
        self.assertLess(
            script.index("xsModifyObjectTasks(629, 1, -6);"),
            script.index("xsModifyObjectTasks(629, 1, -3);"),
        )

        trigger = scenario.trigger_manager.triggers[0]
        self.assertEqual(
            [{"message": "unit_modifier_tasks_0();"}],
            trigger.new_effect.script_call_calls,
        )

        modifier.create_triggers()
        self.assertEqual(1, len(scenario.xs_manager.scripts))
        self.assertEqual(1, len(trigger.new_effect.script_call_calls))

        with self.assertRaises(RuntimeError):
            modifier.add_task(refund)

    def test_explicit_insert_indices_are_consecutive_for_multiple_targets(self) -> None:
        scenario = _FakeScenario()
        task = GarrisonTask(affected_objects=TaskTargets.object_ids([82, 109]))

        UnitModifier(scenario, 279, 1).add_task(task, insertion_index=3).create_triggers()
        script = scenario.xs_manager.scripts[0]["xs_string"]

        self.assertIn("xsModifyObjectTasks(279, 1, 3);", script)
        self.assertIn("xsModifyObjectTasks(279, 1, 4);", script)

    def test_edit_requires_one_index_per_rendered_target(self) -> None:
        scenario = _FakeScenario()
        task = GarrisonTask(affected_objects=TaskTargets.object_ids([82, 109]))

        with self.assertRaises(ValueError):
            UnitModifier(scenario, 279, 1).edit_task(task, task_indices=[3])

    def test_existing_attribute_effect_behavior_is_preserved(self) -> None:
        scenario = _FakeScenario()
        modifier = UnitModifier(scenario, 4, 1)

        modifier.modify_attribute(ObjectAttribute.ATTACK, 0, 5, armor_attack_class=3).create_triggers()

        call = scenario.trigger_manager.triggers[0].new_effect.modify_attribute_calls[0]
        self.assertIsNone(call["quantity"])
        self.assertEqual(5, call["armour_attack_quantity"])
        self.assertEqual(3, call["armour_attack_class"])
        self.assertEqual([], scenario.xs_manager.scripts)

    def test_task_indices_must_be_valid_and_unique(self) -> None:
        scenario = _FakeScenario()
        modifier = UnitModifier(scenario, 4, 1)

        with self.assertRaises(ValueError):
            modifier.remove_task(-1)
        with self.assertRaises(ValueError):
            modifier.remove_tasks([1, 1])
        with self.assertRaises(ValueError):
            modifier.add_task(GarrisonTask(), insertion_index=-1)

    def test_consecutive_single_removals_are_combined_in_descending_order(self) -> None:
        scenario = _FakeScenario()

        UnitModifier(scenario, 4, 1).remove_task(2).remove_task(5).create_triggers()
        script = scenario.xs_manager.scripts[0]["xs_string"]

        self.assertLess(
            script.index("xsModifyObjectTasks(4, 1, -6);"),
            script.index("xsModifyObjectTasks(4, 1, -3);"),
        )


if __name__ == "__main__":
    unittest.main()
