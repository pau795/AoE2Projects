from AoE2ScenarioParser.datasets.players import PlayerId
from AoE2ScenarioParser.datasets.projectiles import ProjectileInfo
from AoE2ScenarioParser.datasets.trigger_lists import Operation, ObjectAttribute, AttackStance, ActionType, \
    CombatAbility, DamageClass, ProjectileSmartMode, ProjectileVanishMode, ProjectileHitMode, FogVisibility
from AoE2ScenarioParser.datasets.units import UnitInfo
from AoE2ScenarioParser.objects.managers.trigger_manager import TriggerManager
from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario
from AoE2ScenarioParser.scenarios.support.data_triggers import DataTriggers


class RespawnAttackGround:

    def __init__(self, scenario: AoE2DEScenario, trigger_data: DataTriggers):
        self.trigger_manager: TriggerManager = scenario.trigger_manager
        self.trigger_data = trigger_data
        self.heavy_scorpion_stats()
        self.heavy_scorpion_tasks()
        self.photon_stats()
        self.photon_stance()
        self.photon_tasks()

    def heavy_scorpion_stats(self):
        scorpion_stats = self.trigger_manager.add_trigger("P8 Heavy Scorpion Attributes")

        # attack ground ability
        scorpion_stats.new_effect.modify_attribute(
            object_list_unit_id=UnitInfo.HEAVY_SCORPION.ID,
            source_player=PlayerId.EIGHT,
            object_attributes=ObjectAttribute.COMBAT_ABILITY,
            operation=Operation.SET,
            quantity=CombatAbility.ATTACK_GROUND)

        scorpion_stats.new_effect.modify_attribute(
            object_list_unit_id=UnitInfo.HEAVY_SCORPION.ID,
            source_player=PlayerId.EIGHT,
            object_attributes=ObjectAttribute.FOG_VISIBILITY,
            operation=Operation.SET,
            quantity=FogVisibility.ALWAYS_VISIBLE)

        # range
        scorpion_stats.new_effect.modify_attribute(
            object_list_unit_id=UnitInfo.HEAVY_SCORPION.ID,
            source_player=PlayerId.EIGHT,
            object_attributes=ObjectAttribute.MAX_RANGE,
            operation=Operation.SET,
            quantity=20)

        scorpion_stats.new_effect.modify_attribute(
            object_list_unit_id=UnitInfo.HEAVY_SCORPION.ID,
            source_player=PlayerId.EIGHT,
            object_attributes=ObjectAttribute.MINIMUM_RANGE,
            operation=Operation.SET,
            quantity=0)

        scorpion_stats.new_effect.modify_attribute(
            object_list_unit_id=UnitInfo.HEAVY_SCORPION.ID,
            source_player=PlayerId.EIGHT,
            object_attributes=ObjectAttribute.SHOWN_RANGE,
            operation=Operation.SET,
            quantity=20)

        # fire projectile
        scorpion_stats.new_effect.modify_attribute(
            object_list_unit_id=UnitInfo.HEAVY_SCORPION.ID,
            source_player=PlayerId.EIGHT,
            object_attributes=ObjectAttribute.PROJECTILE_UNIT,
            operation=Operation.SET,
            quantity=ProjectileInfo.HEAVY_SCORPION_FIRE.ID)

        # damage
        scorpion_stats.new_effect.modify_attribute(
            object_list_unit_id=UnitInfo.HEAVY_SCORPION.ID,
            source_player=PlayerId.EIGHT,
            object_attributes=ObjectAttribute.ATTACK,
            operation=Operation.SET,
            armour_attack_class=DamageClass.BASE_PIERCE,
            armour_attack_quantity=25)

        scorpion_stats.new_effect.modify_attribute(
            object_list_unit_id=UnitInfo.HEAVY_SCORPION.ID,
            source_player=PlayerId.EIGHT,
            object_attributes=ObjectAttribute.SHOWN_ATTACK,
            operation=Operation.SET,
            quantity=25)

        # reload time
        scorpion_stats.new_effect.modify_attribute(
            object_list_unit_id=UnitInfo.HEAVY_SCORPION.ID,
            source_player=PlayerId.EIGHT,
            object_attributes=ObjectAttribute.ATTACK_RELOAD_TIME,
            operation=Operation.SET,
            quantity=2)

        # projectile full damage
        scorpion_stats.new_effect.modify_attribute(
            object_list_unit_id=ProjectileInfo.HEAVY_SCORPION_FIRE.ID,
            source_player=PlayerId.EIGHT,
            object_attributes=ObjectAttribute.PROJECTILE_SMART_MODE,
            operation=Operation.SET,
            quantity=ProjectileSmartMode.FULL_DAMAGE_ON_MISSED_HIT)

        scorpion_stats.new_effect.modify_attribute(
            object_list_unit_id=ProjectileInfo.HEAVY_SCORPION_FIRE.ID,
            source_player=PlayerId.EIGHT,
            object_attributes=ObjectAttribute.TERRAIN_RESTRICTION_ID,
            operation=Operation.SET,
            quantity=26)

        scorpion_stats.new_effect.modify_attribute(
            object_list_unit_id=ProjectileInfo.HEAVY_SCORPION_FIRE.ID,
            source_player=PlayerId.EIGHT,
            object_attributes=ObjectAttribute.FOG_VISIBILITY,
            operation=Operation.SET,
            quantity=FogVisibility.ALWAYS_VISIBLE)

    def heavy_scorpion_tasks(self):
        scorpion_task = self.trigger_manager.add_trigger("P8 Heavy Scorpion Tasks")
        scorpion_list = self.trigger_data.objects['scorpions']
        scorpion_targets = self.trigger_data.tiles['scorpions_target']
        for i, scorpion in enumerate(scorpion_list):

            # no attack
            scorpion_task.new_effect.change_object_stance(
                selected_object_ids=scorpion.reference_id,
                source_player=PlayerId.EIGHT,
                attack_stance=AttackStance.NO_ATTACK_STANCE)

            # disable targeting
            scorpion_task.new_effect.disable_unit_targeting(
                selected_object_ids=scorpion.reference_id,
                source_player=PlayerId.EIGHT)

            scorpion_task.new_effect.task_object(
                selected_object_ids=scorpion.reference_id,
                source_player=PlayerId.EIGHT,
                action_type=ActionType.ATTACK_GROUND,
                location_x=scorpion_targets[i].x,
                location_y=scorpion_targets[i].y)

    def photon_stats(self):
        photon_stats = self.trigger_manager.add_trigger("P8 Photon Man Attributes")

        # attack ground ability
        photon_stats.new_effect.modify_attribute(
            object_list_unit_id=UnitInfo.PHOTONMAN.ID,
            source_player=PlayerId.EIGHT,
            object_attributes=ObjectAttribute.COMBAT_ABILITY,
            operation=Operation.SET,
            quantity=CombatAbility.ATTACK_GROUND)

        # damage
        photon_stats.new_effect.modify_attribute(
            object_list_unit_id=UnitInfo.PHOTONMAN.ID,
            source_player=PlayerId.EIGHT,
            object_attributes=ObjectAttribute.ATTACK,
            operation=Operation.SET,
            armour_attack_class=DamageClass.BASE_PIERCE,
            armour_attack_quantity=25)

        # reload time
        photon_stats.new_effect.modify_attribute(
            object_list_unit_id=UnitInfo.PHOTONMAN.ID,
            source_player=PlayerId.EIGHT,
            object_attributes=ObjectAttribute.ATTACK_RELOAD_TIME,
            operation=Operation.SET,
            quantity=3)

        # no blast damage
        photon_stats.new_effect.modify_attribute(
            object_list_unit_id=UnitInfo.PHOTONMAN.ID,
            source_player=PlayerId.EIGHT,
            object_attributes=ObjectAttribute.BLAST_WIDTH,
            operation=Operation.SET,
            quantity=0)

        photon_stats.new_effect.modify_attribute(
            object_list_unit_id=UnitInfo.PHOTONMAN.ID,
            source_player=PlayerId.EIGHT,
            object_attributes=ObjectAttribute.SHOWN_ATTACK,
            operation=Operation.SET,
            quantity=25)

        photon_stats.new_effect.modify_attribute(
            object_list_unit_id=UnitInfo.PHOTONMAN.ID,
            source_player=PlayerId.EIGHT,
            object_attributes=ObjectAttribute.FOG_VISIBILITY,
            operation=Operation.SET,
            quantity=FogVisibility.ALWAYS_VISIBLE)

        photon_stats.new_effect.modify_attribute(
            object_list_unit_id=UnitInfo.PHOTONMAN.ID,
            source_player=PlayerId.EIGHT,
            object_attributes=ObjectAttribute.PROJECTILE_UNIT,
            operation=Operation.SET,
            quantity=ProjectileInfo.CANNON_GALLEON.ID)

        # projectile full damage
        photon_stats.new_effect.modify_attribute(
            object_list_unit_id=ProjectileInfo.CANNON_GALLEON.ID,
            source_player=PlayerId.EIGHT,
            object_attributes=ObjectAttribute.PROJECTILE_SMART_MODE,
            operation=Operation.SET,
            quantity=ProjectileSmartMode.FULL_DAMAGE_ON_MISSED_HIT)

        photon_stats.new_effect.modify_attribute(
            object_list_unit_id=ProjectileInfo.CANNON_GALLEON.ID,
            source_player=PlayerId.EIGHT,
            object_attributes=ObjectAttribute.FOG_VISIBILITY,
            operation=Operation.SET,
            quantity=FogVisibility.ALWAYS_VISIBLE)

        # projectile arc
        photon_stats.new_effect.modify_attribute(
            object_list_unit_id=ProjectileInfo.CANNON_GALLEON.ID,
            source_player=PlayerId.EIGHT,
            object_attributes=ObjectAttribute.PROJECTILE_ARC,
            operation=Operation.SET,
            quantity=0)

        # hit mode
        photon_stats.new_effect.modify_attribute(
            object_list_unit_id=ProjectileInfo.CANNON_GALLEON.ID,
            source_player=PlayerId.EIGHT,
            object_attributes=ObjectAttribute.PROJECTILE_HIT_MODE,
            operation=Operation.SET,
            quantity=ProjectileHitMode.ANY_PLAYER_UNIT)

        # movement speed
        photon_stats.new_effect.modify_attribute(
            object_list_unit_id=ProjectileInfo.CANNON_GALLEON.ID,
            source_player=PlayerId.EIGHT,
            object_attributes=ObjectAttribute.MOVEMENT_SPEED,
            operation=Operation.SET,
            quantity=3)

        # pass_trough
        photon_stats.new_effect.modify_attribute(
            object_list_unit_id=ProjectileInfo.CANNON_GALLEON.ID,
            source_player=PlayerId.EIGHT,
            object_attributes=ObjectAttribute.PROJECTILE_VANISH_MODE,
            operation=Operation.SET,
            quantity=ProjectileVanishMode.PASS_THROUGH)

        photon_stats.new_effect.modify_attribute(
            object_list_unit_id=ProjectileInfo.CANNON_GALLEON.ID,
            source_player=PlayerId.EIGHT,
            object_attributes=ObjectAttribute.TERRAIN_RESTRICTION_ID,
            operation=Operation.SET,
            quantity=26)

    def photon_stance(self):
        photon_stance = self.trigger_manager.add_trigger("P8 Photon Man Stance")
        photon_list = self.trigger_data.objects['photons']
        photon_targets = self.trigger_data.tiles['photons_target']
        for i, photon in enumerate(photon_list):

            # no attack
            photon_stance.new_effect.change_object_stance(
                selected_object_ids=photon.reference_id,
                source_player=PlayerId.EIGHT,
                attack_stance=AttackStance.NO_ATTACK_STANCE)

            # disable targeting
            photon_stance.new_effect.disable_unit_targeting(
                selected_object_ids=photon.reference_id,
                source_player=PlayerId.EIGHT)

    def photon_tasks(self):
        photon_list = self.trigger_data.objects['photons']
        photon_targets = self.trigger_data.tiles['photons_target']

        firsts = [0, 1, 2, 5, 7]
        seconds = [3,]
        thirds = [4, 6, 8]

        photon_firsts = self.trigger_manager.add_trigger("P8 Photon Man Tasks Firsts")
        photon_firsts.new_condition.timer(timer=2)
        for i in firsts:
            photon_firsts.new_effect.task_object(
                selected_object_ids=photon_list[i].reference_id,
                source_player=PlayerId.EIGHT,
                action_type=ActionType.ATTACK_GROUND,
                location_x=photon_targets[i].x,
                location_y=photon_targets[i].y)

        photon_seconds = self.trigger_manager.add_trigger("P8 Photon Man Tasks Seconds")
        photon_seconds.new_condition.timer(timer=3)
        for i in seconds:
            photon_seconds.new_effect.task_object(
                selected_object_ids=photon_list[i].reference_id,
                source_player=PlayerId.EIGHT,
                action_type=ActionType.ATTACK_GROUND,
                location_x=photon_targets[i].x,
                location_y=photon_targets[i].y)

        photon_thirds = self.trigger_manager.add_trigger("P8 Photon Man Tasks Thirds")
        photon_thirds.new_condition.timer(timer=4)
        for i in thirds:
            photon_thirds.new_effect.task_object(
                selected_object_ids=photon_list[i].reference_id,
                source_player=PlayerId.EIGHT,
                action_type=ActionType.ATTACK_GROUND,
                location_x=photon_targets[i].x,
                location_y=photon_targets[i].y)

        # create a function that takes an Area of the Scenario and copies it into another area

