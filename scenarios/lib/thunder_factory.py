import math
import random

from AoE2ScenarioParser.datasets.buildings import BuildingInfo
from AoE2ScenarioParser.datasets.other import OtherInfo
from AoE2ScenarioParser.datasets.players import PlayerId
from AoE2ScenarioParser.datasets.trigger_lists import Operation, ObjectState, Comparison, ObjectAttribute, ColorMood, CombatAbility, FogVisibility
from AoE2ScenarioParser.objects.data_objects.terrain_tile import TerrainTile
from AoE2ScenarioParser.objects.data_objects.trigger import Trigger
from AoE2ScenarioParser.objects.managers.trigger_manager import TriggerManager
from AoE2ScenarioParser.objects.support.area import Area
from AoE2ScenarioParser.objects.support.tile import Tile

from scenarios.lib.equally_probable_trigger_list import FastEquallyProbableTriggerList
from scenarios.lib.unit_modifier import UnitModifier
from scenarios.lib.xs.unit_tasks import AuraTask, TaskTargets
from scenarios.lib.xs.xs_constants import XsConstantEffectAmount, XsConstantObjectClass


class ThunderFactory:
    SPARK_SOUNDS = ["static_electricity_1", "static_electricity_2", "static_electricity_3"]
    LIGHTNING_SOUND = ["lightning_bolt_2", "lightning_bolt_3"]
    MAX_LIGHTNING_TIME = 150
    COLOR_MOOD_VARIABLE = 102

    def __init__(self, scenario, player_list: list[PlayerId], lightning_damage: int, spark_timing: int, time_to_lightning: int):
        self.scenario = scenario
        self.trigger_manager: TriggerManager = scenario.trigger_manager
        self.player_list = player_list
        self.lightning_damage = lightning_damage
        self.spark_timing = spark_timing
        self.cloud_timing = spark_timing * 2
        self.time_to_lightning = time_to_lightning
        self.time_to_sparks = time_to_lightning - self.spark_timing
        self.time_to_cloud = time_to_lightning - self.cloud_timing
        self.color_mood_trigger = self.set_color_mood()

        init_variables = self.trigger_manager.add_trigger(f"Initialize Color Mood")
        init_variables.new_effect.change_variable(
            variable=self.COLOR_MOOD_VARIABLE,
            operation=Operation.SET,
            quantity=0
        )

    def set_color_mood(self):
        color_mood_trigger = self.trigger_manager.add_trigger('Color Mood', enabled=False)
        color_mood_trigger.new_condition.variable_value(
            variable=self.COLOR_MOOD_VARIABLE,
            comparison=Comparison.EQUAL,
            quantity=0
        )
        color_mood_trigger.new_effect.change_color_mood(
            color_mood=ColorMood.NIGHT,
            quantity=1
        )
        color_mood_trigger.new_effect.change_variable(
            variable=self.COLOR_MOOD_VARIABLE,
            operation=Operation.SET,
            quantity=1
        )
        reset_color_mood = self.trigger_manager.add_trigger('Reset Color Mood', enabled=False)
        reset_color_mood.new_condition.timer(timer=self.spark_timing + 5)
        reset_color_mood.new_effect.change_color_mood(
            color_mood=ColorMood.DEFAULT,
            quantity=1
        )
        reset_color_mood.new_effect.change_variable(
            variable=self.COLOR_MOOD_VARIABLE,
            operation=Operation.SET,
            quantity=0
        )
        reset_color_mood.new_effect.deactivate_trigger(
            color_mood_trigger.trigger_id
        )
        color_mood_trigger.new_effect.activate_trigger(
            trigger_id=reset_color_mood.trigger_id
        )
        return color_mood_trigger

    def set_thunder_flags(self):
        (UnitModifier(self.scenario, BuildingInfo.WOODEN_BRIDGE_B_MIDDLE.ID, PlayerId.GAIA)
         .modify_attribute(ObjectAttribute.UNIT_SIZE_X, Operation.SET, 0)
         .modify_attribute(ObjectAttribute.UNIT_SIZE_Y, Operation.SET, 0)
         .modify_attribute(ObjectAttribute.UNIT_SIZE_Z, Operation.SET, 0)
         .modify_attribute(ObjectAttribute.STANDING_GRAPHIC, Operation.SET, 10636)
         .modify_attribute(ObjectAttribute.DYING_GRAPHIC, Operation.SET, 4151)
         .modify_attribute(ObjectAttribute.DEAD_UNIT_ID, Operation.SET, OtherInfo.FLAG_B.ID)
         .modify_attribute(ObjectAttribute.HIT_POINTS, Operation.SET, 2)
         .modify_attribute(ObjectAttribute.COMBAT_ABILITY, Operation.SET, CombatAbility.ENABLE_AURA_ABILITY)
         .modify_attribute(ObjectAttribute.DAMAGE_GRAPHICS_TOTAL_NUM, Operation.SET, 0)
         .modify_attribute(ObjectAttribute.FOUNDATION_TERRAIN, Operation.SET, -1)
         .modify_attribute(ObjectAttribute.TRAIN_TIME, Operation.SET, 0)
         .modify_attribute(ObjectAttribute.FOG_VISIBILITY, Operation.SET, FogVisibility.NOT_VISIBLE)
         .add_task(AuraTask(
            affected_objects=TaskTargets(True, [XsConstantObjectClass.ARCHER_CLASS, XsConstantObjectClass.ARTIFACT_CLASS,
                                                XsConstantObjectClass.TRADE_BOAT_CLASS, XsConstantObjectClass.VILLAGER_CLASS, XsConstantObjectClass.INFANTRY_CLASS,
                                                XsConstantObjectClass.MISCELLANEOUS_CLASS, XsConstantObjectClass.CAVALRY_CLASS, XsConstantObjectClass.SIEGE_WEAPON_CLASS,
                                                XsConstantObjectClass.TERRAIN_CLASS, XsConstantObjectClass.HEALER_CLASS, XsConstantObjectClass.MONK_CLASS,
                                                XsConstantObjectClass.TRADE_CART_CLASS, XsConstantObjectClass.TRANSPORT_SHIP_CLASS, XsConstantObjectClass.FISHING_BOAT_CLASS,
                                                XsConstantObjectClass.WARSHIP_CLASS, XsConstantObjectClass.CONQUISTADOR_CLASS, XsConstantObjectClass.WAR_ELEPHANT_CLASS,
                                                XsConstantObjectClass.HERO_CLASS, XsConstantObjectClass.ELEPHANT_ARCHER_CLASS, XsConstantObjectClass.PHALANX_CLASS,
                                                XsConstantObjectClass.DOMESTIC_ANIMAL_CLASS, XsConstantObjectClass.PETARD_CLASS, XsConstantObjectClass.CAVALRY_ARCHER_CLASS,
                                                XsConstantObjectClass.DOPPELGANGER_CLASS, XsConstantObjectClass.MONK_WITH_RELIC_CLASS,
                                                XsConstantObjectClass.HAND_CANNONEER_CLASS, XsConstantObjectClass.TWO_HANDED_SWORDSMAN_CLASS,
                                                XsConstantObjectClass.PIKEMAN_CLASS, XsConstantObjectClass.SCOUT_CAVALRY_CLASS, XsConstantObjectClass.SPEARMAN_CLASS,
                                                XsConstantObjectClass.PACKED_UNIT_CLASS, XsConstantObjectClass.BOARDING_SHIP_CLASS, XsConstantObjectClass.UNPACKED_SIEGE_UNIT_CLASS,
                                                XsConstantObjectClass.SCORPION_CLASS, XsConstantObjectClass.RAIDER_CLASS, XsConstantObjectClass.CAVALRY_RAIDER_CLASS,
                                                XsConstantObjectClass.KING_CLASS, XsConstantObjectClass.BUILDING_CLASS, XsConstantObjectClass.WALL_CLASS,
                                                XsConstantObjectClass.TOWER_CLASS, XsConstantObjectClass.GATE_CLASS, XsConstantObjectClass.FARM_CLASS]),
            modifier_value=-(self.lightning_damage * 60),
            modified_attribute=XsConstantEffectAmount.REGENERATION_RATE,
            minimum_units_in_range=1,
            effect_range=3,
            flags=AuraTask.Flags.CIRCULAR | AuraTask.Flags.VISIBLE_RANGE,
            target_ownership=AuraTask.Ownership.ALL,
        ))
         .create_triggers()
         )
        (UnitModifier(self.scenario, OtherInfo.FLAG_B.ID, PlayerId.GAIA)
         .modify_attribute(ObjectAttribute.STANDING_GRAPHIC, Operation.SET, 10638)
         .modify_attribute(ObjectAttribute.FOG_VISIBILITY, Operation.SET, FogVisibility.NOT_VISIBLE)
         .modify_attribute(ObjectAttribute.HIT_POINTS, Operation.SET, 10)
         .create_triggers()
         )
        (UnitModifier(self.scenario, OtherInfo.FLAG_C.ID, PlayerId.GAIA)
         .modify_attribute(ObjectAttribute.STANDING_GRAPHIC, Operation.SET, 10637)
         .modify_attribute(ObjectAttribute.MINIMAP_MODE, Operation.SET, 3)
         .modify_attribute(ObjectAttribute.FOG_VISIBILITY, Operation.SET, FogVisibility.NOT_VISIBLE)
         .modify_attribute(ObjectAttribute.HIT_POINTS, Operation.SET, 2)
         .create_triggers()
         )
        (UnitModifier(self.scenario, OtherInfo.ROCK_FORMATION_2.ID, PlayerId.GAIA)
         .modify_attribute(ObjectAttribute.DEAD_UNIT_ID, Operation.SET, 143)
         .create_triggers()
         )
        (UnitModifier(self.scenario, OtherInfo.FLAG_L.ID, PlayerId.GAIA)
         .modify_attribute(ObjectAttribute.STANDING_GRAPHIC, Operation.SET, 10643)
         .create_triggers()
         )
        (UnitModifier(self.scenario, OtherInfo.FLAG_S.ID, PlayerId.GAIA)
         .modify_attribute(ObjectAttribute.STANDING_GRAPHIC, Operation.SET, 10645)
         .create_triggers()
         )

    def set_thunder_flag_damage(self):
        flag_damage = self.trigger_manager.add_trigger('Damage Flags', looping=True)
        flags = [BuildingInfo.WOODEN_BRIDGE_B_MIDDLE.ID, OtherInfo.FLAG_B.ID, OtherInfo.FLAG_C.ID]
        for flag in flags:
            flag_damage.new_effect.damage_object(
                source_player=PlayerId.GAIA,
                object_list_unit_id=flag,
                quantity=1
            )

    def generate_sound_effects(self, name: str, sound_tile: Tile, sound_effects: list[str]) -> list[Trigger]:
        sound_trigger_list = []
        for sound_id in sound_effects:
            avalanche_sound_trigger = self.trigger_manager.add_trigger(f"{name} sound {sound_id}", enabled=False)
            for player in self.player_list:
                avalanche_sound_trigger.new_effect.play_sound(
                    source_player=player,
                    sound_name=sound_id,
                    location_x=sound_tile.x,
                    location_y=sound_tile.y,
                    global_sound=True
                )
            sound_trigger_list.append(avalanche_sound_trigger)
        FastEquallyProbableTriggerList(sound_trigger_list)
        return sound_trigger_list

    def set_thunder_zone(self, thunder_zone: Area, zone_id: int):
        zone_counter_variable = zone_id * 4
        cloud_timer_variable = zone_id * 4 + 1
        spark_timer_variable = zone_id * 4 + 2
        lightning_timer_variable = zone_id * 4 + 3
        self.trigger_manager.add_variable(f'thunder_dune_{zone_id}_counter', zone_counter_variable)
        self.trigger_manager.add_variable(f'thunder_dune_{zone_id}_cloud_timer', cloud_timer_variable)
        self.trigger_manager.add_variable(f'thunder_dune_{zone_id}_spark_timer', spark_timer_variable)
        self.trigger_manager.add_variable(f'thunder_dune_{zone_id}_lightning_timer', lightning_timer_variable)

        init_variables = self.trigger_manager.add_trigger(f"Initialize Thunder Zone {zone_id}")
        init_variables.new_effect.change_variable(
            variable=zone_counter_variable,
            operation=Operation.SET,
            quantity=0
        )
        init_variables.new_effect.change_variable(
            variable=cloud_timer_variable,
            operation=Operation.SET,
            quantity=self.time_to_cloud
        )
        init_variables.new_effect.change_variable(
            variable=spark_timer_variable,
            operation=Operation.SET,
            quantity=self.time_to_sparks
        )
        init_variables.new_effect.change_variable(
            variable=lightning_timer_variable,
            operation=Operation.SET,
            quantity=self.time_to_lightning
        )

        lightning_timer_max_trigger = self.trigger_manager.add_trigger(f"Thunder Zone {zone_id} Lightning Timer MAX", looping=True)
        lightning_timer_max_trigger.new_condition.variable_value(
            variable=lightning_timer_variable,
            comparison=Comparison.LARGER,
            quantity=self.MAX_LIGHTNING_TIME
        )
        lightning_timer_max_trigger.new_effect.change_variable(
            variable=lightning_timer_variable,
            operation=Operation.SET,
            quantity=self.MAX_LIGHTNING_TIME
        )
        lightning_timer_max_trigger.new_effect.change_variable(
            variable=cloud_timer_variable,
            operation=Operation.SET,
            quantity=self.MAX_LIGHTNING_TIME - self.cloud_timing
        )
        lightning_timer_max_trigger.new_effect.change_variable(
            variable=spark_timer_variable,
            operation=Operation.SET,
            quantity=self.MAX_LIGHTNING_TIME - self.spark_timing
        )

        # COUNTER CONDITIONS
        zone_with_units = self.trigger_manager.add_trigger(f"Thunder Zone {zone_id} Units", looping=True)
        zone_with_units.new_condition.compare_variables(
            variable=zone_counter_variable,
            variable2=spark_timer_variable,
            comparison=Comparison.LARGER_OR_EQUAL
        )
        zone_with_units.new_condition.and_()
        zone_with_units.new_condition.compare_variables(
            variable=zone_counter_variable,
            variable2=lightning_timer_variable,
            comparison=Comparison.LESS
        )
        for player in self.player_list:
            zone_with_units.new_condition.or_()
            zone_with_units.new_condition.objects_in_area(
                quantity=1,
                source_player=player,
                area_x1=thunder_zone.x1,
                area_y1=thunder_zone.y1,
                area_x2=thunder_zone.x2,
                area_y2=thunder_zone.y2,
                object_state=ObjectState.ALIVE,
                inverted=False
            )
        zone_with_units.new_effect.change_variable(
            variable=zone_counter_variable,
            quantity=1,
            operation=Operation.ADD,
        )

        spark_sounds_triggers = self.generate_sound_effects("Sparks", Tile(int(thunder_zone.get_center()[0]), int(thunder_zone.get_center()[1])), self.SPARK_SOUNDS)
        lightning_sounds_triggers = self.generate_sound_effects("Lightning", Tile(int(thunder_zone.get_center()[0]), int(thunder_zone.get_center()[1])), self.LIGHTNING_SOUND)

        # CLOUDS
        zone_clouds = self.trigger_manager.add_trigger(f"Thunder Zone Clouds")
        zone_clouds.new_condition.compare_variables(
            variable=zone_counter_variable,
            variable2=cloud_timer_variable,
            comparison=Comparison.EQUAL
        )
        zone_clouds.new_effect.create_object(
            source_player=PlayerId.GAIA,
            object_list_unit_id=OtherInfo.FLAG_S.ID,
            location_x=int(thunder_zone.get_center()[0]),
            location_y=int(thunder_zone.get_center()[1]),
        )

        # SPARKS
        zone_sparks = self.trigger_manager.add_trigger(f"Thunder Zone Sparks", looping=True)
        zone_sparks.new_condition.compare_variables(
            variable=zone_counter_variable,
            variable2=spark_timer_variable,
            comparison=Comparison.LARGER_OR_EQUAL
        )
        zone_sparks.new_condition.compare_variables(
            variable=zone_counter_variable,
            variable2=lightning_timer_variable,
            comparison=Comparison.LESS
        )
        spark_tiles = self.get_even_distribution(thunder_zone, 15)
        for tile in spark_tiles:
            zone_sparks.new_effect.create_object(
                source_player=PlayerId.GAIA,
                object_list_unit_id=OtherInfo.FLAG_C.ID,
                location_x=tile.x,
                location_y=tile.y,
            )
        for sound in spark_sounds_triggers:
            zone_sparks.new_effect.activate_trigger(sound.trigger_id)
        zone_sparks.new_effect.activate_trigger(self.color_mood_trigger.trigger_id)

        # LIGHTNING
        lightning_delay = self.trigger_manager.add_trigger(f"Thunder Zone Lightning Delay", enabled=False)
        lightning_start = self.trigger_manager.add_trigger(f"Thunder Zone Lightning", looping=True)
        lightning_start.new_condition.compare_variables(
            variable=zone_counter_variable,
            variable2=lightning_timer_variable,
            comparison=Comparison.EQUAL
        )
        lightning_start.new_effect.change_variable(
            variable=zone_counter_variable,
            operation=Operation.SET,
            quantity=0
        )
        lightning_start.new_effect.change_variable(
            variable=spark_timer_variable,
            operation=Operation.ADD,
            quantity=10
        )
        lightning_start.new_effect.change_variable(
            variable=cloud_timer_variable,
            operation=Operation.ADD,
            quantity=10
        )
        lightning_start.new_effect.change_variable(
            variable=lightning_timer_variable,
            operation=Operation.ADD,
            quantity=10
        )
        lightning_tiles = self.get_even_distribution(thunder_zone, 15)
        for tile in lightning_tiles:
            lightning_delay.new_effect.create_object(
                source_player=PlayerId.GAIA,
                object_list_unit_id=BuildingInfo.WOODEN_BRIDGE_B_MIDDLE.ID,
                location_x=tile.x,
                location_y=tile.y,
            )
        lightning_delay.new_effect.kill_object(
            object_list_unit_id=OtherInfo.ROCK_FORMATION_2.ID,
            source_player=PlayerId.GAIA,
            area_x1=thunder_zone.x1,
            area_y1=thunder_zone.y1,
            area_x2=thunder_zone.x2,
            area_y2=thunder_zone.y2,
        )
        lightning_delay.new_effect.remove_object(
            object_list_unit_id=OtherInfo.FLAG_S.ID,
            source_player=PlayerId.GAIA,
            area_x1=thunder_zone.x1,
            area_y1=thunder_zone.y1,
            area_x2=thunder_zone.x2,
            area_y2=thunder_zone.y2,
        )
        lightning_delay.new_effect.activate_trigger(zone_clouds.trigger_id)
        for sound in lightning_sounds_triggers:
            lightning_start.new_effect.activate_trigger(sound.trigger_id)
        lightning_start.new_effect.activate_trigger(lightning_delay.trigger_id)

    @staticmethod
    def get_even_distribution(thunder_area: Area, samples: int) -> list[Tile]:
        tiles = thunder_area.to_coords()
        selected = [random.choice(tiles)]

        remaining: set[None | Tile | TerrainTile] = set(tiles)
        remaining.remove(selected[0])

        while len(selected) < samples and remaining:

            best_tile = None
            best_dist = -1

            for tile in remaining:
                if not tile:
                    continue
                d = min(math.hypot(tile.x - s.x, tile.y - s.y) for s in selected)

                if d > best_dist:
                    best_dist = d
                    best_tile = tile

            selected.append(best_tile)
            remaining.remove(best_tile)

        return selected
