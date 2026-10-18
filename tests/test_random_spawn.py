import unittest
from types import SimpleNamespace

from AoE2ScenarioParser.datasets.players import PlayerId

from scenarios.lib.random_spawn import RandomSpawn


class _CallRecorder:
    def __init__(self):
        self.calls = []

    def __getattr__(self, method_name):
        def record(*args, **kwargs):
            self.calls.append((method_name, args, kwargs))

        return record


class _FakeTrigger:
    def __init__(self, trigger_id, name, **kwargs):
        self.trigger_id = trigger_id
        self.name = name
        self.settings = kwargs
        self.new_condition = _CallRecorder()
        self.new_effect = _CallRecorder()


class _FakeTriggerManager:
    def __init__(self):
        self.triggers = []

    def add_trigger(self, name, **kwargs):
        trigger = _FakeTrigger(len(self.triggers), name, **kwargs)
        self.triggers.append(trigger)
        return trigger


class _FakeUnitManager:
    def __init__(self):
        self.removed_reference_ids = []

    def remove_unit(self, reference_id):
        self.removed_reference_ids.append(reference_id)


def _four_zone_relation():
    zones = [f"zone{index}" for index in range(1, 5)]
    return {
        PlayerId.ONE: {
            source_zone: {
                PlayerId.TWO: [zone for zone in zones if zone != source_zone]
            }
            for source_zone in zones
        }
    }


def _four_zone_objects():
    return {
        f"RS_zone{index}_gold_1": [
            SimpleNamespace(
                unit_const=66,
                x=index,
                y=index,
                player=PlayerId.ONE,
                reference_id=index,
            )
        ]
        for index in range(1, 5)
    }


class RandomSpawnTests(unittest.TestCase):
    def test_four_zones_create_a_second_random_choice_for_the_target_player(self):
        scenario = SimpleNamespace(
            trigger_manager=_FakeTriggerManager(),
            unit_manager=_FakeUnitManager(),
        )
        data_triggers = SimpleNamespace(objects=_four_zone_objects())

        RandomSpawn(
            scenario,
            data_triggers,
            [PlayerId.ONE, PlayerId.TWO],
            _four_zone_relation(),
        )

        parent = next(
            trigger
            for trigger in scenario.trigger_manager.triggers
            if trigger.name == "Activate P1 zone1"
        )
        target_choices = [
            trigger
            for trigger in scenario.trigger_manager.triggers
            if trigger.name.endswith("for P1 zone1")
        ]

        self.assertEqual(3, len(target_choices))
        self.assertEqual(
            [33, 50, 100],
            [
                call[2]["chance"] if "chance" in call[2] else call[1][0]
                for trigger in target_choices
                for call in trigger.new_condition.calls
                if call[0] == "chance"
            ],
        )
        parent_activated_ids = {
            call[1][0] if call[1] else call[2]["trigger_id"]
            for call in parent.new_effect.calls
            if call[0] == "activate_trigger"
        }
        self.assertTrue(
            {trigger.trigger_id for trigger in target_choices}.issubset(parent_activated_ids)
        )

    def test_relation_sanity_requires_every_other_zone(self):
        relation = _four_zone_relation()
        relation[PlayerId.ONE]["zone1"][PlayerId.TWO].remove("zone4")

        with self.assertRaisesRegex(ValueError, "missing remaining zones.*zone4"):
            RandomSpawn._normalize_zone_relation(
                relation,
                [PlayerId.ONE, PlayerId.TWO],
                {f"zone{index}": {} for index in range(1, 5)},
            )

    def test_legacy_single_zone_values_are_normalized(self):
        normalized = RandomSpawn._normalize_zone_relation(
            {
                PlayerId.ONE: {
                    "zone1": {PlayerId.TWO: "zone2"},
                    "zone2": {PlayerId.TWO: "zone1"},
                }
            },
            [PlayerId.ONE, PlayerId.TWO],
            {"zone1": {}, "zone2": {}},
        )

        self.assertEqual(
            ["zone2"], normalized[PlayerId.ONE]["zone1"][PlayerId.TWO]
        )


if __name__ == "__main__":
    unittest.main()
