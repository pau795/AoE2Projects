from AoE2ScenarioParser.datasets.other import OtherInfo
from AoE2ScenarioParser.datasets.players import PlayerId
from AoE2ScenarioParser.datasets.projectiles import ProjectileInfo
from AoE2ScenarioParser.datasets.trigger_lists import ActionType, ObjectAttribute, Operation, AttackStance, TerrainRestrictions, CombatAbility, ProjectileHitMode, \
    ProjectileVanishMode, ProjectileSmartMode, ObstructionType, BlockageClass
from AoE2ScenarioParser.datasets.units import UnitInfo
from AoE2ScenarioParser.objects.data_objects.trigger import Trigger
from AoE2ScenarioParser.objects.support.tile import Tile

from scenarios.lib.equally_probable_trigger_list import EquallyProbableTriggerList
from scenarios.lib.parser_project import ParserProject
from scenarios.lib.unit_modifier import UnitModifier
from scenarios.lib.xs.xs_constants import XsConstantDamageClass, XsConstantEffectAmount


class Avalanche(ParserProject):
    AVALANCHE_UNIT_LIST = [UnitInfo.MILITIA.ID, UnitInfo.MAN_AT_ARMS.ID, UnitInfo.LONG_SWORDSMAN.ID, UnitInfo.TWO_HANDED_SWORDSMAN.ID]
    AVALANCHE_SOUNDS = ["avalanche_1", "avalanche_2", "avalanche_3"]
    AVALANCHE_PLAYER = PlayerId.THREE

    def __init__(self, input_scenario_name: str, output_scenario_name: str):
        super().__init__(input_scenario_name, output_scenario_name)
        self.trigger_manager = self.scenario.trigger_manager
        self.map_manager = self.scenario.map_manager
        self.unit_manager = self.scenario.unit_manager
        self.xs_manager = self.scenario.xs_manager
        self.data_triggers = self.scenario.actions.load_data_triggers()
        self.player_list = [PlayerId.ONE, PlayerId.TWO]
        self.remove_units_trigger = self.remove_units()

    def remove_units(self) -> Trigger:
        remove_units = self.trigger_manager.add_trigger("Remove Units")
        remove_units.new_condition.timer(5)
        for unit_id in self.AVALANCHE_UNIT_LIST:
            remove_units.new_effect.remove_object(
                source_player=self.AVALANCHE_PLAYER,
                object_list_unit_id=unit_id
            )
        return remove_units

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

    def stop_avalanches(self):
        stop_avalanche_trigger = self.trigger_manager.add_trigger("Stop Avalanche", looping=True)
        for tile in self.scenario.new.area().select_entire_map().to_coords(as_terrain=True):
            if tile.elevation == 0:
                stop_avalanche_trigger.new_effect.kill_object(
                    source_player=self.AVALANCHE_PLAYER,
                    area_x1=tile.x,
                    area_y1=tile.y,
                    area_x2=tile.x,
                    area_y2=tile.y,
                )

    def generate_avalanches(self, corner_tile: Tile, avalanche_tile: Tile) -> Trigger:
        generate_units = self.trigger_manager.add_trigger("Generate Units", enabled=False)
        units_attack_ground = self.trigger_manager.add_trigger("Units Attack Ground", enabled=False)
        for unit_id in self.AVALANCHE_UNIT_LIST:
            generate_units.new_effect.create_object(
                object_list_unit_id=unit_id,
                source_player=self.AVALANCHE_PLAYER,
                location_x=corner_tile.x,
                location_y=corner_tile.y,
                disable_sound=True,
            )
            generate_units.new_effect.disable_unit_targeting(
                object_list_unit_id=unit_id,
                source_player=self.AVALANCHE_PLAYER,
                area_x1=corner_tile.x,
                area_y1=corner_tile.y,
                area_x2=corner_tile.x,
                area_y2=corner_tile.y,
            )
            generate_units.new_effect.disable_object_selection(
                object_list_unit_id=unit_id,
                source_player=self.AVALANCHE_PLAYER,
                area_x1=corner_tile.x,
                area_y1=corner_tile.y,
                area_x2=corner_tile.x,
                area_y2=corner_tile.y,
            ),
            generate_units.new_effect.change_object_stance(
                object_list_unit_id=unit_id,
                source_player=self.AVALANCHE_PLAYER,
                area_x1=corner_tile.x,
                area_y1=corner_tile.y,
                area_x2=corner_tile.x,
                area_y2=corner_tile.y,
                attack_stance=AttackStance.NO_ATTACK_STANCE
            )
            units_attack_ground.new_effect.task_object(
                object_list_unit_id=unit_id,
                source_player=self.AVALANCHE_PLAYER,
                area_x1=corner_tile.x,
                area_y1=corner_tile.y,
                area_x2=corner_tile.x,
                area_y2=corner_tile.y,
                location_x=avalanche_tile.x,
                location_y=avalanche_tile.y,
                action_type=ActionType.ATTACK_GROUND
            )
        generate_units.new_effect.activate_trigger(units_attack_ground.trigger_id)
        units_attack_ground.new_effect.activate_trigger(self.remove_units_trigger.trigger_id)
        return generate_units

    def replace_rock(self):
        replace_rock_trigger = self.trigger_manager.add_trigger("Replace Rock", looping=True)
        damage_rock = self.trigger_manager.add_trigger("Damage Rock", looping=True)
        replace_rock_trigger.new_effect.replace_object(
            source_player=self.AVALANCHE_PLAYER,
            target_player=PlayerId.GAIA,
            object_list_unit_id=OtherInfo.FLAG_A.ID,
            object_list_unit_id_2=OtherInfo.FLAG_A.ID
        )
        replace_rock_trigger.new_effect.replace_object(
            source_player=PlayerId.GAIA,
            target_player=PlayerId.GAIA,
            object_list_unit_id=OtherInfo.FLAG_A.ID,
            object_list_unit_id_2=OtherInfo.SEA_ROCKS_1.ID
        )
        damage_rock.new_effect.damage_object(
            object_list_unit_id=OtherInfo.SEA_ROCKS_1.ID,
            source_player=PlayerId.GAIA,
            quantity=1
        )

    def unit_stats(self):
        graphic_dict = {
            UnitInfo.MILITIA.ID: (ProjectileInfo.ARC.ID, 10639, 0.5, 7),
            UnitInfo.MAN_AT_ARMS.ID: (ProjectileInfo.CROSSBOWMAN.ID, 10640, 0.5, 7),
            UnitInfo.LONG_SWORDSMAN.ID: (ProjectileInfo.LONGBOWMAN.ID, 10641, 0.5, 7),
            UnitInfo.TWO_HANDED_SWORDSMAN.ID: (ProjectileInfo.ACA.ID, 10642, 1.0, 4)
        }
        for unit_id, (projectile_id, projectile_graphic_id, projectile_size, num_projectiles) in graphic_dict.items():
            (UnitModifier(self.scenario, unit_id, self.AVALANCHE_PLAYER)
             .modify_attribute(ObjectAttribute.HIT_POINTS, Operation.SET, 20000)
             .modify_attribute(ObjectAttribute.INVULNERABILITY_LEVEL, Operation.SET, -20000)
             .modify_attribute(ObjectAttribute.UNIT_SIZE_X, Operation.SET, 0)
             .modify_attribute(ObjectAttribute.UNIT_SIZE_Y, Operation.SET, 0)
             .modify_attribute(ObjectAttribute.UNIT_SIZE_Z, Operation.SET, 0)
             .modify_attribute(ObjectAttribute.STANDING_GRAPHIC, Operation.SET, 0)
             .modify_attribute(ObjectAttribute.WALKING_GRAPHIC, Operation.SET, 0)
             .modify_attribute(ObjectAttribute.ATTACK_GRAPHIC, Operation.SET, 10638)
             .modify_attribute(ObjectAttribute.ATTACK_GRAPHIC_2, Operation.SET, 0)
             .modify_attribute(ObjectAttribute.IDLE_ATTACK_GRAPHIC, Operation.SET, 0)
             .modify_attribute(ObjectAttribute.DYING_GRAPHIC, Operation.SET, 0)
             .modify_attribute_xs(ObjectAttribute.PROJECTILE_GRAPHIC_DISPLACEMENT_X, Operation.SET, 0)
             .modify_attribute_xs(ObjectAttribute.PROJECTILE_GRAPHIC_DISPLACEMENT_Y, Operation.SET, 0)
             .modify_attribute_xs(ObjectAttribute.PROJECTILE_GRAPHIC_DISPLACEMENT_Z, Operation.SET, 0.01)
             .modify_attribute_xs(ObjectAttribute.ATTACK, Operation.SET, 500, XsConstantDamageClass.MELEE)
             .modify_attribute(ObjectAttribute.PROJECTILE_SPAWNING_AREA_WIDTH, Operation.SET, 2)
             .modify_attribute(ObjectAttribute.PROJECTILE_SPAWNING_AREA_LENGTH, Operation.SET, 2)
             .modify_attribute(ObjectAttribute.ATTACK_RELOAD_TIME, Operation.SET, 10)
             .modify_attribute(ObjectAttribute.PROJECTILE_SPAWNING_AREA_RANDOMNESS, Operation.SET, 1)
             .modify_attribute(ObjectAttribute.DEAD_UNIT_ID, Operation.SET, -1)
             .modify_attribute(ObjectAttribute.TERRAIN_RESTRICTION_ID, Operation.SET, TerrainRestrictions.ALL)
             .modify_attribute(ObjectAttribute.MOVEMENT_SPEED, Operation.SET, 0)
             .modify_attribute(ObjectAttribute.MAXIMUM_RANGE, Operation.SET, 300)
             .modify_attribute(ObjectAttribute.LINE_OF_SIGHT, Operation.SET, 300)
             .modify_attribute(ObjectAttribute.COMBAT_ABILITY, Operation.SET, CombatAbility.ATTACK_GROUND | CombatAbility.BULK_VOLLEY_RELEASE)
             .modify_attribute(ObjectAttribute.TOTAL_MISSILES, Operation.SET, num_projectiles)
             .modify_attribute(ObjectAttribute.MAXIMUM_TOTAL_MISSILES, Operation.SET, num_projectiles)
             .modify_attribute(ObjectAttribute.PROJECTILE_UNIT, Operation.SET, projectile_id)
             .modify_attribute(ObjectAttribute.SECONDARY_PROJECTILE_UNIT, Operation.SET, -1)
             .modify_attribute(ObjectAttribute.ACCURACY_PERCENT, Operation.SET, 0)
             .modify_attribute(ObjectAttribute.ATTACK_DISPERSION, Operation.SET, 0.25)
             .create_triggers())
            (UnitModifier(self.scenario, projectile_id, self.AVALANCHE_PLAYER)
             .modify_attribute(ObjectAttribute.UNIT_SIZE_X, Operation.SET, projectile_size)
             .modify_attribute(ObjectAttribute.UNIT_SIZE_Y, Operation.SET, projectile_size)
             .modify_attribute(ObjectAttribute.UNIT_SIZE_Z, Operation.SET, 100.0)
             .modify_attribute(ObjectAttribute.STANDING_GRAPHIC, Operation.SET, projectile_graphic_id)
             .modify_attribute(ObjectAttribute.WALKING_GRAPHIC, Operation.SET, projectile_graphic_id)
             .modify_attribute(ObjectAttribute.DYING_GRAPHIC, Operation.SET, 12181)
             .modify_attribute(ObjectAttribute.DEAD_UNIT_ID, Operation.SET, OtherInfo.FLAG_A.ID)
             .modify_attribute(ObjectAttribute.FOG_VISIBILITY, Operation.SET, 1)
             .modify_attribute(ObjectAttribute.BLAST_ATTACK_LEVEL, Operation.SET, 1)
             .modify_attribute(ObjectAttribute.TRAILING_UNIT, Operation.SET, 247)
             .modify_attribute(ObjectAttribute.TRAIL_MODE, Operation.SET, 2)
             .modify_attribute_xs(XsConstantEffectAmount.TRAIL_DENSITY, Operation.SET, 0.5)
             .modify_attribute(ObjectAttribute.TRAILING_UNIT, Operation.SET, 247)
             .modify_attribute(ObjectAttribute.MOVEMENT_SPEED, Operation.SET, 2)
             .modify_attribute(ObjectAttribute.PROJECTILE_HIT_MODE, Operation.SET, ProjectileHitMode.ANY_PLAYER_UNIT)
             .modify_attribute(ObjectAttribute.PROJECTILE_VANISH_MODE, Operation.SET, ProjectileVanishMode.PASS_THROUGH | ProjectileVanishMode.ALWAYS_SPAWN_DEAD_UNIT)
             .modify_attribute(ObjectAttribute.PROJECTILE_SMART_MODE, Operation.SET, ProjectileSmartMode.FULL_DAMAGE_ON_MISSED_HIT)
             .modify_attribute_xs(ObjectAttribute.PROJECTILE_ARC, Operation.SET, 0)
             .create_triggers())
            (UnitModifier(self.scenario, OtherInfo.FLAG_A.ID, self.AVALANCHE_PLAYER)
             .modify_attribute(ObjectAttribute.STANDING_GRAPHIC, Operation.SET, 10644)
             .create_triggers())
            (UnitModifier(self.scenario, OtherInfo.FLAG_A.ID, PlayerId.GAIA)
             .modify_attribute(ObjectAttribute.STANDING_GRAPHIC, Operation.SET, 10644)
             .create_triggers())
            (UnitModifier(self.scenario, OtherInfo.SEA_ROCKS_1.ID, PlayerId.GAIA)
             .modify_attribute(ObjectAttribute.STANDING_GRAPHIC, Operation.SET, 10644)
             .modify_attribute(ObjectAttribute.HIT_POINTS, Operation.SET, 100)
             .modify_attribute(ObjectAttribute.UNIT_SIZE_X, Operation.SET, 0.5)
             .modify_attribute(ObjectAttribute.UNIT_SIZE_Y, Operation.SET, 0.5)
             .modify_attribute(ObjectAttribute.UNIT_SIZE_Z, Operation.SET, 1)
             .modify_attribute(ObjectAttribute.OBSTRUCTION_TYPE, Operation.SET, ObstructionType.SOLID_SQUARE_OUTLINE_COLLISION)
             .modify_attribute(ObjectAttribute.BLOCKAGE_CLASS, Operation.SET, BlockageClass.RESOURCE)
             .modify_attribute(ObjectAttribute.INTERACTION_MODE, Operation.SET, 2)
             .modify_attribute(ObjectAttribute.DEAD_UNIT_ID, Operation.SET, OtherInfo.ICE_NAVIGABLE.ID)
             .create_triggers())

    def process(self):
        self.xs_manager.initialise_xs_trigger()
        self.unit_stats()
        self.replace_rock()
        self.stop_avalanches()
        top1 = self.data_triggers.tiles['avalanche_top_1']
        top2 = self.data_triggers.tiles['avalanche_top_2']
        top3 = self.data_triggers.tiles['avalanche_top_3']

        top1_triggers = self.generate_avalanches(top1[0], top1[1])
        top2_triggers = self.generate_avalanches(top2[0], top2[1])
        top3_triggers = self.generate_avalanches(top3[0], top3[1])

        avalanche_sound_triggers = self.generate_avalanche_sounds(top1[0])
        sound_probability = EquallyProbableTriggerList(self.trigger_manager, avalanche_sound_triggers, "Random Avalanche Sounds")

        enable_middle = self.trigger_manager.add_trigger("enable_middle")
        enable_middle.new_condition.timer(15)
        enable_middle.new_effect.activate_trigger(sound_probability.enable_probability_trigger.trigger_id)
        enable_middle.new_effect.activate_trigger(top1_triggers.trigger_id)
        enable_middle.new_effect.activate_trigger(top2_triggers.trigger_id)
        enable_middle.new_effect.activate_trigger(top3_triggers.trigger_id)


if __name__ == '__main__':
    avalanche_class = Avalanche(
        input_scenario_name=f'EDIT_AVALANCHE_1V1',
        output_scenario_name=f'OUTPUT_AVALANCHE_1V1',
    )
    avalanche_class.convert()
