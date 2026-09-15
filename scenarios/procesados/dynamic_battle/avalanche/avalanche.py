import math

from AoE2ScenarioParser.datasets.buildings import BuildingInfo
from AoE2ScenarioParser.datasets.other import OtherInfo
from AoE2ScenarioParser.datasets.players import PlayerId
from AoE2ScenarioParser.datasets.trigger_lists import ActionType, ObjectAttribute, Operation, AttackStance, CombatAbility, OcclusionMode, DamageClass, ObjectClass, Comparison
from AoE2ScenarioParser.datasets.units import UnitInfo
from AoE2ScenarioParser.objects.data_objects.trigger import Trigger
from AoE2ScenarioParser.objects.support.area import Area
from AoE2ScenarioParser.objects.support.tile import Tile
from scenarios.lib.equally_probable_trigger_list import EquallyProbableTriggerList
from scenarios.lib.parser_project import ParserProject
from scenarios.lib.unit_modifier import UnitModifier
from scenarios.lib.xs.unit_tasks import TaskTargets, AuraTask
from scenarios.lib.xs.xs_constants import XsConstantEffectAmount, XsConstantObjectClass


class Avalanche(ParserProject):
    PREDATOR_DICT = {
        UnitInfo.TIGER.ID: (UnitInfo.JAGUAR.ID, 10639),
        UnitInfo.DIRE_WOLF.ID: (UnitInfo.GREY_WOLF.ID, 10640),
        UnitInfo.BROWN_BEAR.ID: (UnitInfo.KOMODO_DRAGON.ID, 10641)
    }
    TREE_LIST = [284, 302, 348, 349, 350, 351, 399, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 413, 414, 768, 1051, 1052, 1053, 1054, 1063, 1144, 1146, 1248, 1249,
                 1250, 1347, 1348, 1349, 1350, 1539, 1540, 1541, 1542, 1717, 1984, 2016, 2017, 2025, 2027, 2028, 2567, 2570, 2580, 2583]
    AVALANCHE_SOUNDS = ["avalanche_1", "avalanche_2", "avalanche_3"]
    RS_ZONE_RELATION = {
        PlayerId.ONE: {
            "zone1": {
                PlayerId.TWO: "zone2",
            },
            "zone2": {
                PlayerId.TWO: "zone1",
            },
        }
    }

    def __init__(self, input_scenario_name: str, output_scenario_name: str):
        super().__init__(input_scenario_name, output_scenario_name)
        self.trigger_manager = self.scenario.trigger_manager
        self.map_manager = self.scenario.map_manager
        self.unit_manager = self.scenario.unit_manager
        self.xs_manager = self.scenario.xs_manager
        self.data_triggers = self.scenario.actions.load_data_triggers()
        self.initialize_variable_trigger = self.trigger_manager.add_trigger("Initialize Variables")
        self.player_list = [PlayerId.ONE, PlayerId.TWO]

    def generate_avalanches(self, avalanche_name: str, base_variable_index: int, avalanche_quantity: tuple[int, int, int], avalanche_areas: list[Area], corner_tiles: list[Tile]) -> list[Trigger]:
        triggers = []
        for i, (source_area, destination_tile, num_avalanches) in enumerate(zip(avalanche_areas, corner_tiles, avalanche_quantity)):
            variable_id = base_variable_index + i
            self.trigger_manager.add_variable(f'{avalanche_name} {i}', variable_id)
            self.initialize_variable_trigger.new_effect.change_variable(
                variable=variable_id,
                operation=Operation.SET,
                quantity=0
            )
            unit_list = self.unit_manager.get_units_in_area(
                x1=source_area.x1,
                y1=source_area.y1,
                x2=source_area.x2,
                y2=source_area.y2
            )
            generate_avalanche_units = self.trigger_manager.add_trigger(f"Generate {avalanche_name} {i} Units", enabled=False)
            avalanche_units_move = self.trigger_manager.add_trigger(f"{avalanche_name} {i} Units Move", enabled=False)
            generate_avalanche_units.new_condition.variable_value(
                variable=variable_id,
                comparison=Comparison.LESS_OR_EQUAL,
                quantity=num_avalanches,
            )
            for static_predator_id, (avalanche_predator_id, _) in self.PREDATOR_DICT.items():
                generate_avalanche_units.new_effect.kill_object(
                    object_list_unit_id=static_predator_id,
                    source_player=PlayerId.GAIA,
                    area_x1=source_area.x1,
                    area_y1=source_area.y1,
                    area_x2=source_area.x2,
                    area_y2=source_area.y2,
                )
            generate_avalanche_units.new_effect.change_variable(
                variable=variable_id,
                operation=Operation.ADD,
                quantity=1
            )
            generate_avalanche_units.new_effect.activate_trigger(avalanche_units_move.trigger_id)
            avalanche_units_move.new_condition.timer(2)
            group_target_vector = [(destination_tile.x + 0.5) - source_area.get_center()[0], (destination_tile.y + 0.5) - source_area.get_center()[1]]
            group_target_distance = math.hypot(*group_target_vector)
            group_target_normal_vector = (group_target_vector[0] / group_target_distance, group_target_vector[1] / group_target_distance)
            for unit in [x for x in unit_list if x.unit_const in self.PREDATOR_DICT.keys()]:
                # unit_target_vector = [(destination_tile.x + 0.5) - unit.x, (destination_tile.y + 0.5) - unit.y]
                # # atan2 preserves which side of the group direction the unit is on.
                # # Negating the angle turns the converging unit-to-destination
                # # direction into an equally sized, outward-spreading direction.
                # angle_to_destination = math.atan2(
                #     group_target_vector[0] * unit_target_vector[1] - group_target_vector[1] * unit_target_vector[0],
                #     group_target_vector[0] * unit_target_vector[0] + group_target_vector[1] * unit_target_vector[1],
                # )
                # angle = -angle_to_destination * 3.5
                # unit_vector = (
                #     group_target_normal_vector[0] * math.cos(angle) - group_target_normal_vector[1] * math.sin(angle),
                #     group_target_normal_vector[0] * math.sin(angle) + group_target_normal_vector[1] * math.cos(angle),
                # )
                # unit_vector_distance = (math.sqrt(unit_vector[0] ** 2 + unit_vector[1] ** 2))
                # normal_unit_vector = (unit_vector[0] / unit_vector_distance, unit_vector[1] / unit_vector_distance)

                x, y = unit.x, unit.y
                while 0 <= x < self.map_manager.map_width and 0 <= y < self.map_manager.map_height:
                    x += group_target_normal_vector[0]
                    y += group_target_normal_vector[1]
                x = int(x - group_target_normal_vector[0])
                y = int(y - group_target_normal_vector[1])

                avalanche_units_move.new_effect.task_object(
                    area_x1=int(unit.x),
                    area_y1=int(unit.y),
                    area_x2=int(unit.x),
                    area_y2=int(unit.y),
                    source_player=PlayerId.GAIA,
                    location_x=x,
                    location_y=y,
                    action_type=ActionType.MOVE
                )
                avalanche_units_move.new_effect.activate_trigger(generate_avalanche_units.trigger_id)
            triggers.append(generate_avalanche_units)
        return triggers

    def unit_stats(self):
        (UnitModifier(self.scenario, 2607, PlayerId.GAIA)
         .modify_attribute(ObjectAttribute.UNIT_SIZE_X, Operation.SET, 0.5)
         .modify_attribute(ObjectAttribute.UNIT_SIZE_Y, Operation.SET, 0.5)
         .modify_attribute(ObjectAttribute.UNIT_SIZE_Z, Operation.SET, 0)
         .modify_attribute(ObjectAttribute.HIT_POINTS, Operation.SET, 1000)
         .modify_attribute(ObjectAttribute.INTERACTION_MODE, Operation.SET, 0)
         .modify_attribute(ObjectAttribute.STANDING_GRAPHIC, Operation.SET, 0)
         .modify_attribute(ObjectAttribute.DYING_GRAPHIC, Operation.SET, 0)
         .modify_attribute(ObjectAttribute.BLAST_WIDTH, Operation.SET, 0.1)
         .modify_attribute(ObjectAttribute.BLAST_ATTACK_LEVEL, Operation.SET, 1)
         .modify_attribute(ObjectAttribute.MINIMAP_MODE, Operation.SET, 0)
         .modify_attribute(ObjectAttribute.ARMOR, Operation.SET, 255, DamageClass.BASE_MELEE)
         .modify_attribute(ObjectAttribute.ARMOR, Operation.SET, 255, DamageClass.BASE_PIERCE)
         .create_triggers()
         )
        (UnitModifier(self.scenario, BuildingInfo.WOODEN_BRIDGE_B_MIDDLE.ID, PlayerId.GAIA)
         .modify_attribute(ObjectAttribute.UNIT_SIZE_X, Operation.SET, 0.5)
         .modify_attribute(ObjectAttribute.UNIT_SIZE_Y, Operation.SET, 0.5)
         .modify_attribute(ObjectAttribute.UNIT_SIZE_Z, Operation.SET, 1.0)
         .modify_attribute(ObjectAttribute.OBSTRUCTION_TYPE, Operation.SET, 2)
         .modify_attribute(ObjectAttribute.INTERACTION_MODE, Operation.SET, 0)
         .modify_attribute(ObjectAttribute.SELECTION_EFFECT, Operation.SET, 2)
         .modify_attribute(ObjectAttribute.HIT_POINTS, Operation.SET, 300)
         .modify_attribute(ObjectAttribute.STANDING_GRAPHIC, Operation.SET, 10643)
         .modify_attribute(ObjectAttribute.DYING_GRAPHIC, Operation.SET, 0)
         .modify_attribute(ObjectAttribute.COMBAT_ABILITY, Operation.SET, CombatAbility.ENABLE_AURA_ABILITY)
         .modify_attribute(ObjectAttribute.DAMAGE_GRAPHICS_TOTAL_NUM, Operation.SET, 0)
         .modify_attribute(ObjectAttribute.FOUNDATION_TERRAIN, Operation.SET, -1)
         .modify_attribute(ObjectAttribute.TRAIN_TIME, Operation.SET, 0)
         .modify_attribute(ObjectAttribute.DEAD_UNIT_ID, Operation.SET, OtherInfo.ICE_NAVIGABLE.ID)
         .add_task(AuraTask(
            affected_objects=TaskTargets(False, [predator_id for predator_id, _ in self.PREDATOR_DICT.values()]),
            modifier_value=-99999999,
            effect_range=0.75,
            modified_attribute=XsConstantEffectAmount.REGENERATION_RATE,
            minimum_units_in_range=1,
            target_ownership=AuraTask.Ownership.ALL,
            flags=AuraTask.Flags.VISIBLE_RANGE
         ))
         .create_triggers()
         )
        snowball_acceleration_trigger = self.trigger_manager.add_trigger("Snowball Acceleration & Rock Damage", looping=True)
        for static_predator_id, (avalanche_predator_id, avalanche_graphic_id) in self.PREDATOR_DICT.items():
            (UnitModifier(self.scenario, avalanche_predator_id, PlayerId.GAIA)
             .modify_attribute(ObjectAttribute.HIT_POINTS, Operation.SET, 1000)
             .modify_attribute(ObjectAttribute.UNIT_SIZE_X, Operation.SET, 0)
             .modify_attribute(ObjectAttribute.UNIT_SIZE_Y, Operation.SET, 0)
             .modify_attribute(ObjectAttribute.UNIT_SIZE_Z, Operation.SET, 0)
             .modify_attribute(ObjectAttribute.OCCLUSION_MODE, Operation.SET, OcclusionMode.DISPLAY_OUTLINE)
             .modify_attribute(ObjectAttribute.INTERACTION_MODE, Operation.SET, 0)
             .modify_attribute(ObjectAttribute.STANDING_GRAPHIC, Operation.SET, 10638)
             .modify_attribute(ObjectAttribute.WALKING_GRAPHIC, Operation.SET, avalanche_graphic_id)
             .modify_attribute(ObjectAttribute.ATTACK_GRAPHIC, Operation.SET, avalanche_graphic_id)
             .modify_attribute(ObjectAttribute.DYING_GRAPHIC, Operation.SET, 10638)
             .modify_attribute(ObjectAttribute.DEAD_UNIT_ID, Operation.SET, BuildingInfo.WOODEN_BRIDGE_B_MIDDLE.ID)
             .modify_attribute(ObjectAttribute.FOG_VISIBILITY, Operation.SET, 1)
             .modify_attribute(ObjectAttribute.TERRAIN_RESTRICTION_ID, Operation.SET, 41)
             .modify_attribute(ObjectAttribute.MOVEMENT_SPEED, Operation.SET, 1.2)
             .modify_attribute(ObjectAttribute.COMBAT_ABILITY, Operation.SET, CombatAbility.ENABLE_AURA_ABILITY)
             .modify_attribute(ObjectAttribute.ARMOR, Operation.SET, 255, DamageClass.BASE_MELEE)
             .modify_attribute(ObjectAttribute.ARMOR, Operation.SET, 255, DamageClass.BASE_PIERCE)
             .modify_attribute(164, Operation.SET, DamageClass.PREDATOR_ANIMALS_FE)
             .add_task(AuraTask(
                affected_objects=TaskTargets(True, [XsConstantObjectClass.LAND_MINE_CLASS]),
                modifier_value=-99999999,
                modified_attribute=XsConstantEffectAmount.REGENERATION_RATE,
                minimum_units_in_range=1,
                effect_range=0.75,
                flags=AuraTask.Flags.CIRCULAR | AuraTask.Flags.VISIBLE_RANGE,
                target_ownership=AuraTask.Ownership.ALL,
            ))
             .add_task(AuraTask(
                affected_objects=TaskTargets(True, [XsConstantObjectClass.BUILDING_CLASS, XsConstantObjectClass.WALL_CLASS, XsConstantObjectClass.TOWER_CLASS,
                                                    XsConstantObjectClass.GATE_CLASS]),
                modifier_value=-2000,
                modified_attribute=XsConstantEffectAmount.REGENERATION_RATE,
                minimum_units_in_range=1,
                effect_range=0.75,
                flags=AuraTask.Flags.CIRCULAR | AuraTask.Flags.VISIBLE_RANGE,
                target_ownership=AuraTask.Ownership.ALL,
            ))
             .add_task(AuraTask(
                affected_objects=TaskTargets(True, [XsConstantObjectClass.ARCHER_CLASS, XsConstantObjectClass.ARTIFACT_CLASS, XsConstantObjectClass.TRADE_BOAT_CLASS,
                                                    XsConstantObjectClass.VILLAGER_CLASS, XsConstantObjectClass.INFANTRY_CLASS, XsConstantObjectClass.PREY_ANIMAL_CLASS,
                                                    XsConstantObjectClass.MISCELLANEOUS_CLASS, XsConstantObjectClass.CAVALRY_CLASS, XsConstantObjectClass.SIEGE_WEAPON_CLASS,
                                                    XsConstantObjectClass.TERRAIN_CLASS, XsConstantObjectClass.HEALER_CLASS, XsConstantObjectClass.MONK_CLASS,
                                                    XsConstantObjectClass.TRADE_CART_CLASS, XsConstantObjectClass.TRANSPORT_SHIP_CLASS, XsConstantObjectClass.FISHING_BOAT_CLASS,
                                                    XsConstantObjectClass.WARSHIP_CLASS, XsConstantObjectClass.CONQUISTADOR_CLASS, XsConstantObjectClass.WAR_ELEPHANT_CLASS,
                                                    XsConstantObjectClass.HERO_CLASS, XsConstantObjectClass.ELEPHANT_ARCHER_CLASS, XsConstantObjectClass.PHALANX_CLASS,
                                                    XsConstantObjectClass.DOMESTIC_ANIMAL_CLASS, XsConstantObjectClass.PETARD_CLASS, XsConstantObjectClass.CAVALRY_ARCHER_CLASS,
                                                    XsConstantObjectClass.DOPPELGANGER_CLASS, XsConstantObjectClass.MONK_WITH_RELIC_CLASS,
                                                    XsConstantObjectClass.HAND_CANNONEER_CLASS, XsConstantObjectClass.TWO_HANDED_SWORDSMAN_CLASS,
                                                    XsConstantObjectClass.PIKEMAN_CLASS, XsConstantObjectClass.SCOUT_CAVALRY_CLASS, XsConstantObjectClass.SPEARMAN_CLASS,
                                                    XsConstantObjectClass.PACKED_UNIT_CLASS, XsConstantObjectClass.BOARDING_SHIP_CLASS,
                                                    XsConstantObjectClass.UNPACKED_SIEGE_UNIT_CLASS, XsConstantObjectClass.SCORPION_CLASS, XsConstantObjectClass.RAIDER_CLASS,
                                                    XsConstantObjectClass.CAVALRY_RAIDER_CLASS, XsConstantObjectClass.LIVESTOCK_CLASS, XsConstantObjectClass.KING_CLASS,
                                                    XsConstantObjectClass.CONTROLLED_ANIMAL_CLASS]),
                modifier_value=-1000,
                modified_attribute=XsConstantEffectAmount.REGENERATION_RATE,
                minimum_units_in_range=1,
                effect_range=0.75,
                flags=AuraTask.Flags.CIRCULAR | AuraTask.Flags.VISIBLE_RANGE,
                target_ownership=AuraTask.Ownership.ALL,
            ))
             .create_triggers())
            (UnitModifier(self.scenario, static_predator_id, PlayerId.GAIA)
             .modify_attribute(ObjectAttribute.HIT_POINTS, Operation.SET, 20000)
             .modify_attribute(ObjectAttribute.INVULNERABILITY_LEVEL, Operation.SET, -20000)
             .modify_attribute(ObjectAttribute.UNIT_SIZE_X, Operation.SET, 0)
             .modify_attribute(ObjectAttribute.UNIT_SIZE_Y, Operation.SET, 0)
             .modify_attribute(ObjectAttribute.UNIT_SIZE_Z, Operation.SET, 0)
             .modify_attribute(ObjectAttribute.OCCLUSION_MODE, Operation.SET, OcclusionMode.DISPLAY_OUTLINE)
             .modify_attribute(ObjectAttribute.INTERACTION_MODE, Operation.SET, 0)
             .modify_attribute(ObjectAttribute.STANDING_GRAPHIC, Operation.SET, 0)
             .modify_attribute(ObjectAttribute.WALKING_GRAPHIC, Operation.SET, 0)
             .modify_attribute(ObjectAttribute.ATTACK_GRAPHIC, Operation.SET, 0)
             .modify_attribute(ObjectAttribute.DYING_GRAPHIC, Operation.SET, 0)
             .modify_attribute(ObjectAttribute.DEAD_UNIT_ID, Operation.SET, static_predator_id)
             .modify_attribute(ObjectAttribute.BLOOD_UNIT, Operation.SET, avalanche_predator_id)
             .modify_attribute(ObjectAttribute.FOG_VISIBILITY, Operation.SET, 1)
             .modify_attribute(ObjectAttribute.MOVEMENT_SPEED, Operation.SET, 0)
             .create_triggers())

            snowball_acceleration_trigger.new_condition.timer(3)
            snowball_acceleration_trigger.new_effect.modify_object_attribute(
                object_list_unit_id=avalanche_predator_id,
                source_player=PlayerId.GAIA,
                object_attributes=ObjectAttribute.MOVEMENT_SPEED,
                operation=Operation.ADD,
                quantity=0.10
            )
            snowball_acceleration_trigger.new_effect.damage_object(
                object_list_unit_id=BuildingInfo.WOODEN_BRIDGE_B_MIDDLE.ID,
                source_player=PlayerId.GAIA,
                quantity=1,
            )

    def passive_predators(self):
        passive_predators_trigger = self.trigger_manager.add_trigger("Passive predators", enabled=True, looping=True)
        for static_predator_id, (avalanche_predator_id, _) in self.PREDATOR_DICT.items():
            passive_predators_trigger.new_effect.disable_unit_targeting(
                object_list_unit_id=static_predator_id,
                source_player=PlayerId.GAIA,
            )
            passive_predators_trigger.new_effect.disable_object_selection(
                object_list_unit_id=static_predator_id,
                source_player=PlayerId.GAIA,
            )
            passive_predators_trigger.new_effect.change_object_stance(
                object_list_unit_id=static_predator_id,
                source_player=PlayerId.GAIA,
                attack_stance=AttackStance.NO_ATTACK_STANCE
            )
            passive_predators_trigger.new_effect.disable_unit_targeting(
                object_list_unit_id=avalanche_predator_id,
                source_player=PlayerId.GAIA,
            )
            passive_predators_trigger.new_effect.disable_object_selection(
                object_list_unit_id=avalanche_predator_id,
                source_player=PlayerId.GAIA,
            )
            passive_predators_trigger.new_effect.change_object_stance(
                object_list_unit_id=avalanche_predator_id,
                source_player=PlayerId.GAIA,
                attack_stance=AttackStance.NO_ATTACK_STANCE
            )
            passive_predators_trigger.new_effect.disable_unit_targeting(
                object_list_unit_id=BuildingInfo.WOODEN_BRIDGE_B_MIDDLE.ID,
                source_player=PlayerId.GAIA,
            )
            passive_predators_trigger.new_effect.disable_object_selection(
                object_list_unit_id=BuildingInfo.WOODEN_BRIDGE_B_MIDDLE.ID,
                source_player=PlayerId.GAIA,
            )

    def stop_avalanches(self):
        stop_avalanche_trigger = self.trigger_manager.add_trigger("Stop Avalanche", looping=True)
        for tile in self.scenario.new.area().select_entire_map().to_coords(as_terrain=True):
            if tile.elevation == 0:
                stop_avalanche_trigger.new_effect.kill_object(
                    object_group=ObjectClass.PREDATOR_ANIMAL,
                    source_player=PlayerId.GAIA,
                    area_x1=tile.x,
                    area_y1=tile.y,
                    area_x2=tile.x,
                    area_y2=tile.y,
                )

    def tree_killer(self) -> None:
        for unit in self.unit_manager.get_all_units():
            if unit.unit_const in self.TREE_LIST:
                self.unit_manager.add_unit(
                    player=PlayerId.GAIA,
                    unit_const=2607,
                    x=unit.x,
                    y=unit.y,
                    z=unit.z,
                )

    def generate_avalanche_sounds(self, sound_tile: Tile) -> list[Trigger]:
        avalanche_sounds = []
        for sound_id in self.AVALANCHE_SOUNDS:
            avalanche_sound_trigger = self.trigger_manager.add_trigger("Avalanche sound", enabled=False)
            for player in self.player_list:
                avalanche_sound_trigger.new_effect.play_sound(
                    source_player=player,
                    sound_name=sound_id,
                    location_x=sound_tile.x,
                    location_y=sound_tile.y,
                    global_sound=True
                )
            avalanche_sounds.append(avalanche_sound_trigger)
        return avalanche_sounds

    def generate_sound_triggers(self, tile: Tile) -> Trigger:
        avalanche_sound_triggers = self.generate_avalanche_sounds(tile)
        sound_probability = EquallyProbableTriggerList(self.trigger_manager, avalanche_sound_triggers, "Random Avalanche Sounds")
        return sound_probability.enable_probability_trigger

    def setup_avalanche(self, trigger_name: str, delay: int, triggers_to_enable: list[Trigger]) -> Trigger:
        avalanche_trigger = self.trigger_manager.add_trigger(trigger_name, enabled=True)
        avalanche_trigger.new_condition.timer(delay)
        for trigger in triggers_to_enable:
            avalanche_trigger.new_effect.activate_trigger(trigger.trigger_id)
        return avalanche_trigger

    def avalanche_cicle(self, avalanche_trigger_list: list[Trigger], setup_trigger_list: list[Trigger], period: int, init_variable: int, end_variable: int):
        avalanche_cicle = self.trigger_manager.add_trigger("Avalanche Cicle", enabled=True, looping=True)
        disable_avalanches = self.trigger_manager.add_trigger("Disable Avalanches", enabled=False)
        enable_avalanches = self.trigger_manager.add_trigger("Enable Avalanches", enabled=False)
        avalanche_cicle.new_condition.timer(period)
        for trigger in avalanche_trigger_list:
            disable_avalanches.new_effect.deactivate_trigger(trigger.trigger_id)
        for trigger in setup_trigger_list:
            enable_avalanches.new_effect.activate_trigger(trigger.trigger_id)
        for i in range(init_variable, end_variable):
            disable_avalanches.new_effect.change_variable(
                variable=i,
                operation=Operation.SET,
                quantity=0
            )
        avalanche_cicle.new_effect.activate_trigger(disable_avalanches.trigger_id)
        disable_avalanches.new_effect.activate_trigger(enable_avalanches.trigger_id)

    def process(self):
        self.xs_manager.initialise_xs_trigger()
        self.unit_stats()
        self.tree_killer()
        self.stop_avalanches()
        top_corners = self.data_triggers.tiles['top_corners']
        left_corners = self.data_triggers.tiles['left_corners']
        right_corners = self.data_triggers.tiles['right_corners']
        bottom_corners = self.data_triggers.tiles['bottom_corners']
        top_areas = self.data_triggers.areas['top_areas']
        left_areas = self.data_triggers.areas['left_areas']
        right_areas = self.data_triggers.areas['right_areas']
        bottom_areas = self.data_triggers.areas['bottom_areas']

        top_avalanches = self.generate_avalanches("Top Avalanche", 0,(3, 1, 3), top_areas, [left_corners[0], bottom_corners[1], right_corners[2]])
        left_avalanches = self.generate_avalanches("Left Avalanche", 3,(3, 1, 3), left_areas, [top_corners[0], right_corners[1], bottom_corners[2]])
        right_avalanches = self.generate_avalanches("Right Avalanche", 6,(3, 1, 3), right_areas, [bottom_corners[0], left_corners[1], top_corners[2]])
        bottom_avalanches = self.generate_avalanches("Bottom Avalanche", 9,(3, 1, 3), bottom_areas, [right_corners[0], top_corners[1], left_corners[2]])

        top_sound = self.generate_sound_triggers(top_corners[1])
        bottom_sound = self.generate_sound_triggers(bottom_corners[1])
        left_sound = self.generate_sound_triggers(left_corners[1])
        right_sound = self.generate_sound_triggers(right_corners[1])

        setup_middle = self.setup_avalanche("Middle Avalanche", 120, [top_avalanches[1], bottom_avalanches[1], left_avalanches[1], right_avalanches[1], top_sound, bottom_sound, left_sound, right_sound])
        setup_sides = self.setup_avalanche("Sides Avalanche", 180, [
            top_avalanches[0], top_avalanches[2],
            left_avalanches[0], left_avalanches[2],
            right_avalanches[0], right_avalanches[2],
            bottom_avalanches[0], bottom_avalanches[2],
            top_sound, left_sound, right_sound, bottom_sound
        ])
        avalanche_trigger_list = top_avalanches + left_avalanches + right_avalanches + bottom_avalanches
        setup_trigger_list = [setup_middle, setup_sides]
        self.avalanche_cicle(avalanche_trigger_list, setup_trigger_list, 600, 0, 12)

        self.passive_predators()


if __name__ == '__main__':
    avalanche_class = Avalanche(
        input_scenario_name=f'EDIT_AVALANCHE_1V1',
        output_scenario_name=f'OUTPUT_AVALANCHE_1V1',
    )
    avalanche_class.convert()
