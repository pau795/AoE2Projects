from AoE2ScenarioParser.datasets.other import OtherInfo
from AoE2ScenarioParser.datasets.players import PlayerId
from AoE2ScenarioParser.datasets.projectiles import ProjectileInfo
from AoE2ScenarioParser.datasets.trigger_lists import ObjectAttribute, Operation, CombatAbility, AttackStance, \
    ActionType, DamageClass, ProjectileSmartMode, ObjectState, FogVisibility
from AoE2ScenarioParser.datasets.units import UnitInfo
from AoE2ScenarioParser.objects.managers.trigger_manager import TriggerManager
from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario
from AoE2ScenarioParser.scenarios.support.data_triggers import DataTriggers


class StoneArea:

    def __init__(self, scenario: AoE2DEScenario, trigger_data: DataTriggers):
        self.trigger_manager: TriggerManager = scenario.trigger_manager
        self.trigger_data = trigger_data
        self.crossbows = self.trigger_data.objects['stone_crossbows']
        self.crossbows_target = self.trigger_data.tiles['stone_crossbows_target']
        self.stone_pass = self.trigger_data.areas['stone_pass']
        self.stone_units = self.trigger_data.areas['stone_units']
        self.stone_resource = self.trigger_data.tiles['stone_area_resource'][0]
        self.init_attributes()
        self.spearmen_stats()
        self.spearmen_tasks()
        self.crossbows_stats()
        self.crossbows_tasks()

    def init_attributes(self):
        init_attributes = self.trigger_manager.add_trigger('Stone Area Initial Attributes')

        for units_area in self.stone_units:
            init_attributes.new_effect.change_object_stance(
                source_player=PlayerId.EIGHT,
                area_x1=units_area.x1,
                area_y1=units_area.y1,
                area_x2=units_area.x2,
                area_y2=units_area.y2,
                attack_stance=AttackStance.NO_ATTACK_STANCE
            )

            init_attributes.new_effect.disable_unit_targeting(
                source_player=PlayerId.EIGHT,
                area_x1=units_area.x1,
                area_y1=units_area.y1,
                area_x2=units_area.x2,
                area_y2=units_area.y2
            )

        spawn_stone = self.trigger_manager.add_trigger("Stone Area Spawn Stone", looping=True)

        spawn_stone.new_condition.objects_in_area(
            object_list=OtherInfo.STONE_MINE.ID,
            source_player=PlayerId.GAIA,
            area_x1=self.stone_resource.x,
            area_y1=self.stone_resource.y,
            area_x2=self.stone_resource.x,
            area_y2=self.stone_resource.y,
            object_state=ObjectState.RESOURCE,
            inverted=True,
            quantity=1
        )

        spawn_stone.new_effect.modify_attribute(
            object_list_unit_id=OtherInfo.STONE_MINE.ID,
            source_player=PlayerId.GAIA,
            object_attributes=ObjectAttribute.AMOUNT_OF_1ST_RESOURCE_STORAGE,
            operation=Operation.SET,
            quantity=500
        )

        spawn_stone.new_effect.create_object(
            object_list_unit_id=OtherInfo.STONE_MINE.ID,
            location_x=self.stone_resource.x,
            location_y=self.stone_resource.y,
            source_player=PlayerId.GAIA
        )

    def spearmen_stats(self):
        stone_spearmen = self.trigger_manager.add_trigger("P8 Stone Spearmen")

        stone_spearmen.new_effect.modify_attribute(
            object_list_unit_id=UnitInfo.SPEARMAN.ID,
            source_player=PlayerId.EIGHT,
            object_attributes=ObjectAttribute.UNIT_SIZE_X,
            operation=Operation.SET,
            quantity=95)
        stone_spearmen.new_effect.modify_attribute(
            object_list_unit_id=UnitInfo.SPEARMAN.ID,
            source_player=PlayerId.EIGHT,
            object_attributes=ObjectAttribute.UNIT_SIZE_X,
            operation=Operation.DIVIDE,
            quantity=100)
        stone_spearmen.new_effect.modify_attribute(
            object_list_unit_id=UnitInfo.SPEARMAN.ID,
            source_player=PlayerId.EIGHT,
            object_attributes=ObjectAttribute.FOG_VISIBILITY,
            operation=Operation.SET,
            quantity=FogVisibility.ALWAYS_VISIBLE)
        stone_spearmen.new_effect.modify_attribute(
            object_list_unit_id=UnitInfo.SPEARMAN.ID,
            source_player=PlayerId.EIGHT,
            object_attributes=ObjectAttribute.UNIT_SIZE_Y,
            operation=Operation.SET,
            quantity=95)
        stone_spearmen.new_effect.modify_attribute(
            object_list_unit_id=UnitInfo.SPEARMAN.ID,
            source_player=PlayerId.EIGHT,
            object_attributes=ObjectAttribute.UNIT_SIZE_Y,
            operation=Operation.DIVIDE,
            quantity=100)

        stone_spearmen.new_effect.modify_attribute(
            object_list_unit_id=UnitInfo.SPEARMAN.ID,
            source_player=PlayerId.EIGHT,
            object_attributes=ObjectAttribute.UNIT_SIZE_Z,
            operation=Operation.SET,
            quantity=5)

        stone_spearmen.new_effect.modify_attribute(
            object_list_unit_id=UnitInfo.SPEARMAN.ID,
            source_player=PlayerId.EIGHT,
            object_attributes=ObjectAttribute.WALKING_GRAPHIC,
            operation=Operation.SET,
            quantity=8250)

        stone_spearmen.new_effect.modify_attribute(
            object_list_unit_id=UnitInfo.SPEARMAN.ID,
            source_player=PlayerId.EIGHT,
            object_attributes=ObjectAttribute.STANDING_GRAPHIC,
            operation=Operation.SET,
            quantity=8250)

        stone_spearmen.new_effect.modify_attribute(
            object_list_unit_id=UnitInfo.SPEARMAN.ID,
            source_player=PlayerId.EIGHT,
            object_attributes=ObjectAttribute.ATTACK_GRAPHIC,
            operation=Operation.SET,
            quantity=8250)

    def spearmen_tasks(self):
        spearman_patrol_trigger = self.trigger_manager.add_trigger("P8 Stone Spearman Tasks")
        spearman = self.trigger_data.objects['stone_spearman']
        spearman_patrol = self.trigger_data.tiles['stone_spearman_patrol']
        for i, spear in enumerate(spearman):
            # no attack
            spearman_patrol_trigger.new_effect.change_object_stance(
                selected_object_ids=spear.reference_id,
                source_player=PlayerId.EIGHT,
                attack_stance=AttackStance.NO_ATTACK_STANCE)

            # disable targeting
            spearman_patrol_trigger.new_effect.disable_unit_targeting(
                selected_object_ids=spear.reference_id,
                source_player=PlayerId.EIGHT)

            spearman_patrol_trigger.new_effect.disable_object_selection(
                selected_object_ids=spear.reference_id,
                source_player=PlayerId.ONE)

            spearman_patrol_trigger.new_effect.task_object(
                selected_object_ids=spear.reference_id,
                source_player=PlayerId.EIGHT,
                action_type=ActionType.PATROL,
                location_x=spearman_patrol[i].x,
                location_y=spearman_patrol[i].y)

    def crossbows_stats(self):
        stone_crossbows = self.trigger_manager.add_trigger("P8 Stone Crossbows")

        stone_crossbows.new_effect.modify_attribute(
            object_list_unit_id=UnitInfo.CROSSBOWMAN.ID,
            source_player=PlayerId.EIGHT,
            object_attributes=ObjectAttribute.FOG_VISIBILITY,
            operation=Operation.SET,
            quantity=FogVisibility.ALWAYS_VISIBLE)
        stone_crossbows.new_effect.modify_attribute(
            object_list_unit_id=UnitInfo.CROSSBOWMAN.ID,
            source_player=PlayerId.EIGHT,
            object_attributes=ObjectAttribute.ATTACK_RELOAD_TIME,
            operation=Operation.SET,
            quantity=50)

        stone_crossbows.new_effect.modify_attribute(
            object_list_unit_id=UnitInfo.CROSSBOWMAN.ID,
            source_player=PlayerId.EIGHT,
            object_attributes=ObjectAttribute.ATTACK_RELOAD_TIME,
            operation=Operation.DIVIDE,
            quantity=100)

        stone_crossbows.new_effect.modify_attribute(
            object_list_unit_id=UnitInfo.CROSSBOWMAN.ID,
            source_player=PlayerId.EIGHT,
            object_attributes=ObjectAttribute.COMBAT_ABILITY,
            operation=Operation.SET,
            quantity=CombatAbility.ATTACK_GROUND + CombatAbility.BULK_VOLLEY_RELEASE)

        stone_crossbows.new_effect.modify_attribute(
            object_list_unit_id=UnitInfo.CROSSBOWMAN.ID,
            source_player=PlayerId.EIGHT,
            object_attributes=ObjectAttribute.MAX_RANGE,
            operation=Operation.SET,
            quantity=30)

        stone_crossbows.new_effect.modify_attribute(
            object_list_unit_id=UnitInfo.CROSSBOWMAN.ID,
            source_player=PlayerId.EIGHT,
            object_attributes=ObjectAttribute.MAX_TOTAL_MISSILES,
            operation=Operation.SET,
            quantity=100)

        stone_crossbows.new_effect.modify_attribute(
            object_list_unit_id=UnitInfo.CROSSBOWMAN.ID,
            source_player=PlayerId.EIGHT,
            object_attributes=ObjectAttribute.TOTAL_MISSILES,
            operation=Operation.SET,
            quantity=100)

        stone_crossbows.new_effect.modify_attribute(
            object_list_unit_id=UnitInfo.CROSSBOWMAN.ID,
            source_player=PlayerId.EIGHT,
            object_attributes=ObjectAttribute.ACCURACY_PERCENT,
            operation=Operation.SET,
            quantity=0)

        stone_crossbows.new_effect.modify_attribute(
            object_list_unit_id=UnitInfo.CROSSBOWMAN.ID,
            source_player=PlayerId.EIGHT,
            object_attributes=ObjectAttribute.ATTACK_DISPERSION,
            operation=Operation.SET,
            quantity=3)

        stone_crossbows.new_effect.modify_attribute(
            object_list_unit_id=UnitInfo.CROSSBOWMAN.ID,
            source_player=PlayerId.EIGHT,
            object_attributes=ObjectAttribute.ATTACK_DISPERSION,
            operation=Operation.SET,
            quantity=3)

        stone_crossbows.new_effect.modify_attribute(
            object_list_unit_id=UnitInfo.CROSSBOWMAN.ID,
            source_player=PlayerId.EIGHT,
            object_attributes=ObjectAttribute.SHOWN_ATTACK,
            operation=Operation.SET,
            quantity=1)

        stone_crossbows.new_effect.modify_attribute(
            object_list_unit_id=UnitInfo.CROSSBOWMAN.ID,
            source_player=PlayerId.EIGHT,
            object_attributes=ObjectAttribute.SHOWN_RANGE,
            operation=Operation.SET,
            quantity=30)

        stone_crossbows.new_effect.modify_attribute(
            object_list_unit_id=UnitInfo.CROSSBOWMAN.ID,
            source_player=PlayerId.EIGHT,
            object_attributes=ObjectAttribute.ATTACK,
            operation=Operation.SET,
            armour_attack_class=DamageClass.BASE_PIERCE,
            armour_attack_quantity=10)

        stone_crossbows.new_effect.modify_attribute(
            object_list_unit_id=UnitInfo.CROSSBOWMAN.ID,
            source_player=PlayerId.EIGHT,
            object_attributes=ObjectAttribute.PROJECTILE_UNIT,
            operation=Operation.SET,
            quantity=ProjectileInfo.WAR_GALLEY_FIRE.ID)

        stone_crossbows.new_effect.modify_attribute(
            object_list_unit_id=ProjectileInfo.WAR_GALLEY_FIRE.ID,
            source_player=PlayerId.EIGHT,
            object_attributes=ObjectAttribute.PROJECTILE_ARC,
            operation=Operation.SET,
            quantity=0)

        stone_crossbows.new_effect.modify_attribute(
            object_list_unit_id=ProjectileInfo.WAR_GALLEY_FIRE.ID,
            source_player=PlayerId.EIGHT,
            object_attributes=ObjectAttribute.PROJECTILE_HIT_MODE,
            operation=Operation.SET,
            quantity=2)

        stone_crossbows.new_effect.modify_attribute(
            object_list_unit_id=ProjectileInfo.WAR_GALLEY_FIRE.ID,
            source_player=PlayerId.EIGHT,
            object_attributes=ObjectAttribute.FOG_VISIBILITY,
            operation=Operation.SET,
            quantity=FogVisibility.ALWAYS_VISIBLE)

        stone_crossbows.new_effect.modify_attribute(
            object_list_unit_id=ProjectileInfo.WAR_GALLEY_FIRE.ID,
            source_player=PlayerId.EIGHT,
            object_attributes=ObjectAttribute.MOVEMENT_SPEED,
            operation=Operation.SET,
            quantity=7)

        stone_crossbows.new_effect.modify_attribute(
            object_list_unit_id=ProjectileInfo.WAR_GALLEY_FIRE.ID,
            source_player=PlayerId.EIGHT,
            object_attributes=ObjectAttribute.PROJECTILE_SMART_MODE,
            operation=Operation.SET,
            quantity=ProjectileSmartMode.FULL_DAMAGE_ON_MISSED_HIT)

        stone_crossbows.new_effect.modify_attribute(
            object_list_unit_id=ProjectileInfo.WAR_GALLEY_FIRE.ID,
            source_player=PlayerId.EIGHT,
            object_attributes=ObjectAttribute.TERRAIN_RESTRICTION_ID,
            operation=Operation.SET,
            quantity=9)

        stone_crossbows.new_effect.modify_attribute(
            object_list_unit_id=ProjectileInfo.WAR_GALLEY_FIRE.ID,
            source_player=PlayerId.EIGHT,
            object_attributes=ObjectAttribute.DYING_GRAPHIC,
            operation=Operation.SET,
            quantity=0)

    def crossbows_tasks(self):
        crossbows_task_trigger = self.trigger_manager.add_trigger("P8 Stone Crossbows Tasks")
        for i, crossbow in enumerate(self.crossbows):
            # no attack
            crossbows_task_trigger.new_effect.change_object_stance(
                selected_object_ids=crossbow.reference_id,
                source_player=PlayerId.EIGHT,
                attack_stance=AttackStance.NO_ATTACK_STANCE)

            # disable targeting
            crossbows_task_trigger.new_effect.disable_unit_targeting(
                selected_object_ids=crossbow.reference_id,
                source_player=PlayerId.EIGHT)

        self.crossbow_sequence(0, 8, 4)
        self.crossbow_sequence(1, 5, 5)
        self.crossbow_sequence(2, 5, 5)
        self.crossbow_sequence(3, 0, 0)

    def crossbow_sequence(self, i, seconds_attack, seconds_stop):
        crossbows_task_attack_ground = self.trigger_manager.add_trigger(f'P8 Stone Crossbow {i} Attack')
        crossbows_task_attack_stop = self.trigger_manager.add_trigger(f'P8 Stone Crossbow {i} Stop', enabled=False)

        crossbows_task_attack_ground.new_effect.task_object(
            selected_object_ids=self.crossbows[i].reference_id,
            source_player=PlayerId.EIGHT,
            action_type=ActionType.ATTACK_GROUND,
            location_x=self.crossbows_target[i].x,
            location_y=self.crossbows_target[i].y)
        if seconds_stop != 0:
            crossbows_task_attack_ground.new_condition.timer(timer=seconds_stop)
            crossbows_task_attack_ground.new_effect.activate_trigger(trigger_id=crossbows_task_attack_stop.trigger_id)
            crossbows_task_attack_stop.new_condition.timer(timer=seconds_attack)
            crossbows_task_attack_stop.new_effect.stop_object(
                selected_object_ids=self.crossbows[i].reference_id,
                source_player=PlayerId.EIGHT)
            crossbows_task_attack_stop.new_effect.activate_trigger(trigger_id=crossbows_task_attack_ground.trigger_id)
        else:
            self.trigger_manager.remove_trigger(crossbows_task_attack_stop.trigger_id)
