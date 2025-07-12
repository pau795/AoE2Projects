from AoE2ScenarioParser.datasets.other import OtherInfo
from AoE2ScenarioParser.datasets.players import PlayerId
from AoE2ScenarioParser.datasets.projectiles import ProjectileInfo
from AoE2ScenarioParser.datasets.trigger_lists import ObjectAttribute, Operation, DamageClass, ObjectState, \
    AttackStance, TimeUnit, FogVisibility
from AoE2ScenarioParser.datasets.units import UnitInfo
from AoE2ScenarioParser.objects.managers.trigger_manager import TriggerManager
from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario
from AoE2ScenarioParser.scenarios.support.data_triggers import DataTriggers


class LumberjackArea:

    def __init__(self, scenario: AoE2DEScenario, trigger_data: DataTriggers):
        self.trigger_manager: TriggerManager = scenario.trigger_manager
        self.trigger_data = trigger_data
        self.onager = self.trigger_data.objects['lumberjack_onager'][0]
        self.tree_tile = self.trigger_data.tiles['lumberjack_tree'][0]
        self.lumberjack_pass = self.trigger_data.areas['lumberjack_pass']
        self.lumberjack_units = self.trigger_data.areas['lumberjack_units']
        self.init_attributes()
        self.lumberjack_area()

    def init_attributes(self):
        init_attributes = self.trigger_manager.add_trigger('Lumberjack Area Initial Attributes')

        for units_area in self.lumberjack_units:
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

    def lumberjack_area(self):
        lumberjack_area = self.trigger_manager.add_trigger("Lumberjack Area")
        tree_check_resource = self.trigger_manager.add_trigger("Lumberjack Area Tree Resource")
        tree_check_alive = self.trigger_manager.add_trigger("Lumberjack Area Tree Alive", enabled=False)
        timer_tree = self.trigger_manager.add_trigger("Lumberjack Area Tree Timer", enabled=False)

        lumberjack_area.new_effect.modify_attribute(
            object_list_unit_id=OtherInfo.TREE_D.ID,
            source_player=PlayerId.GAIA,
            object_attributes=ObjectAttribute.AMOUNT_OF_1ST_RESOURCE_STORAGE,
            operation=Operation.SET,
            quantity=500
        )

        lumberjack_area.new_effect.modify_attribute(
            object_list_unit_id=OtherInfo.TREE_D.ID,
            source_player=PlayerId.GAIA,
            object_attributes=ObjectAttribute.DEAD_UNIT_ID,
            operation=Operation.SET,
            quantity=OtherInfo.TREE_D.ID
        )

        lumberjack_area.new_effect.modify_attribute(
            object_list_unit_id=OtherInfo.TREE_D.ID,
            source_player=PlayerId.GAIA,
            object_attributes=ObjectAttribute.HIT_POINTS,
            operation=Operation.SET,
            quantity=1000
        )

        lumberjack_area.new_effect.modify_attribute(
            object_list_unit_id=OtherInfo.TREE_D.ID,
            source_player=PlayerId.GAIA,
            object_attributes=ObjectAttribute.UNIT_SIZE_Z,
            operation=Operation.SET,
            quantity=0
        )

        lumberjack_area.new_effect.modify_attribute(
            object_list_unit_id=UnitInfo.SIEGE_ONAGER.ID,
            source_player=PlayerId.EIGHT,
            object_attributes=ObjectAttribute.ATTACK,
            operation=Operation.SET,
            armour_attack_class=DamageClass.BASE_MELEE,
            armour_attack_quantity=400
        )

        lumberjack_area.new_effect.modify_attribute(
            object_list_unit_id=UnitInfo.SIEGE_ONAGER.ID,
            source_player=PlayerId.EIGHT,
            object_attributes=ObjectAttribute.FOG_VISIBILITY,
            operation=Operation.SET,
            quantity=FogVisibility.ALWAYS_VISIBLE
        )
        lumberjack_area.new_effect.modify_attribute(
            object_list_unit_id=UnitInfo.SIEGE_ONAGER.ID,
            source_player=PlayerId.EIGHT,
            object_attributes=ObjectAttribute.PROJECTILE_UNIT,
            operation=Operation.SET,
            quantity=ProjectileInfo.MANGONEL_PRIMARY_FIRE.ID
        )
        lumberjack_area.new_effect.modify_attribute(
            object_list_unit_id=UnitInfo.SIEGE_ONAGER.ID,
            source_player=PlayerId.EIGHT,
            object_attributes=ObjectAttribute.SECONDARY_PROJECTILE_UNIT,
            operation=Operation.SET,
            quantity=ProjectileInfo.MANGONEL_SECONDARY_FIRE.ID
        )
        lumberjack_area.new_effect.modify_attribute(
            object_list_unit_id=ProjectileInfo.MANGONEL_PRIMARY_FIRE.ID,
            source_player=PlayerId.EIGHT,
            object_attributes=ObjectAttribute.FOG_VISIBILITY,
            operation=Operation.SET,
            quantity=FogVisibility.ALWAYS_VISIBLE
        )
        lumberjack_area.new_effect.modify_attribute(
            object_list_unit_id=ProjectileInfo.MANGONEL_SECONDARY_FIRE.ID,
            source_player=PlayerId.EIGHT,
            object_attributes=ObjectAttribute.FOG_VISIBILITY,
            operation=Operation.SET,
            quantity=FogVisibility.ALWAYS_VISIBLE
        )

        lumberjack_area.new_effect.modify_attribute(
            object_list_unit_id=UnitInfo.SIEGE_ONAGER.ID,
            source_player=PlayerId.EIGHT,
            object_attributes=ObjectAttribute.MINIMUM_RANGE,
            operation=Operation.SET,
            quantity=0
        )

        lumberjack_area.new_effect.change_object_stance(
            selected_object_ids=self.onager.reference_id,
            source_player=PlayerId.EIGHT,
            attack_stance=AttackStance.STAND_GROUND
        )

        lumberjack_area.new_effect.disable_unit_targeting(
            object_list_unit_id=UnitInfo.SIEGE_ONAGER.ID,
            source_player=PlayerId.EIGHT,
            selected_object_ids=self.onager.reference_id
        )

        lumberjack_area.new_effect.modify_attribute(
            object_list_unit_id=UnitInfo.SIEGE_ONAGER.ID,
            source_player=PlayerId.EIGHT,
            object_attributes=ObjectAttribute.ATTACK_RELOAD_TIME,
            operation=Operation.SET,
            quantity=15
        )
        lumberjack_area.new_effect.create_object(
            object_list_unit_id=OtherInfo.TREE_D.ID,
            source_player=PlayerId.GAIA,
            location_x=self.tree_tile.x,
            location_y=self.tree_tile.y
        )

        tree_check_resource.new_condition.objects_in_area(
            object_list=OtherInfo.TREE_D.ID,
            source_player=PlayerId.GAIA,
            area_x1=self.tree_tile.x,
            area_y1=self.tree_tile.y,
            area_x2=self.tree_tile.x,
            area_y2=self.tree_tile.y,
            object_state=ObjectState.RESOURCE,
            quantity=1
        )
        tree_check_resource.new_effect.activate_trigger(
            trigger_id=timer_tree.trigger_id
        )
        tree_check_resource.new_effect.activate_trigger(
            trigger_id=tree_check_alive.trigger_id
        )
        tree_check_resource.new_effect.display_timer(
            timer=0,
            display_time=60,
            time_unit=TimeUnit.SECONDS,
            message="Lumberjack Area Tree Reset: %d",
            reset_timer=True
        )

        tree_check_alive.new_condition.objects_in_area(
            object_list=OtherInfo.TREE_D.ID,
            source_player=PlayerId.GAIA,
            area_x1=self.tree_tile.x,
            area_y1=self.tree_tile.y,
            area_x2=self.tree_tile.x,
            area_y2=self.tree_tile.y,
            object_state=ObjectState.ALIVE,
            quantity=1
        )
        tree_check_alive.new_effect.activate_trigger(
            trigger_id=tree_check_resource.trigger_id
        )
        tree_check_alive.new_effect.clear_timer(
            timer=0
        )

        timer_tree.new_condition.display_timer_triggered(
            timer_id=0
        )
        timer_tree.new_effect.remove_object(
            object_list_unit_id=OtherInfo.TREE_D.ID,
            source_player=PlayerId.GAIA,
            area_x1=self.tree_tile.x,
            area_y1=self.tree_tile.y,
            area_x2=self.tree_tile.x,
            area_y2=self.tree_tile.y,
            object_state=ObjectState.RESOURCE
        )
        timer_tree.new_effect.remove_object(
            object_list_unit_id=OtherInfo.TREE_D.ID,
            source_player=PlayerId.GAIA,
            area_x1=self.tree_tile.x,
            area_y1=self.tree_tile.y,
            area_x2=self.tree_tile.x,
            area_y2=self.tree_tile.y,
            object_state=ObjectState.ALIVE
        )
        timer_tree.new_effect.create_object(
            object_list_unit_id=OtherInfo.TREE_D.ID,
            source_player=PlayerId.GAIA,
            location_x=self.tree_tile.x,
            location_y=self.tree_tile.y
        )



