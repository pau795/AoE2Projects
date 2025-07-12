from AoE2ScenarioParser.datasets.other import OtherInfo
from AoE2ScenarioParser.datasets.players import PlayerId
from AoE2ScenarioParser.datasets.trigger_lists import ObjectAttribute, Operation, DamageClass, ObjectState, \
    AttackStance, TerrainRestrictions, FogVisibility
from AoE2ScenarioParser.datasets.units import UnitInfo
from AoE2ScenarioParser.objects.managers.trigger_manager import TriggerManager
from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario
from AoE2ScenarioParser.scenarios.support.data_triggers import DataTriggers


class FishingArea:

    def __init__(self, scenario: AoE2DEScenario, trigger_data: DataTriggers):
        self.trigger_manager: TriggerManager = scenario.trigger_manager
        self.trigger_data = trigger_data
        self.fishing_area = self.trigger_data.areas['fishing_area'][0]
        self.fishing_demo = self.trigger_data.tiles['fishing_demo']
        self.fishing_pass = self.trigger_data.areas['fishing_pass']
        self.fishing_units = self.trigger_data.areas['fishing_units']
        self.initial_stats()
        self.demo_effects()
        self.spawn_demos()

    def initial_stats(self):
        initial_stats = self.trigger_manager.add_trigger("Fishing Area Initial Stats")

        for units_area in self.fishing_units:
            initial_stats.new_effect.change_object_stance(
                source_player=PlayerId.EIGHT,
                area_x1=units_area.x1,
                area_y1=units_area.y1,
                area_x2=units_area.x2,
                area_y2=units_area.y2,
                attack_stance=AttackStance.NO_ATTACK_STANCE
            )

            initial_stats.new_effect.disable_unit_targeting(
                source_player=PlayerId.EIGHT,
                area_x1=units_area.x1,
                area_y1=units_area.y1,
                area_x2=units_area.x2,
                area_y2=units_area.y2
            )

        initial_stats.new_effect.modify_attribute(
            object_list_unit_id=OtherInfo.FISH_SALMON.ID,
            source_player=PlayerId.GAIA,
            object_attributes=ObjectAttribute.TERRAIN_RESTRICTION_ID,
            operation=Operation.SET,
            quantity=TerrainRestrictions.ALL
        )

        initial_stats.new_effect.modify_attribute(
            object_list_unit_id=OtherInfo.FISH_SALMON.ID,
            source_player=PlayerId.GAIA,
            object_attributes=ObjectAttribute.DEAD_UNIT_ID,
            operation=Operation.SET,
            quantity=OtherInfo.FISH_SALMON.ID,
        )

        initial_stats.new_effect.modify_attribute(
            object_list_unit_id=UnitInfo.HEAVY_DEMOLITION_SHIP.ID,
            source_player=PlayerId.EIGHT,
            object_attributes=ObjectAttribute.LINE_OF_SIGHT,
            operation=Operation.SET,
            quantity=20
        )

        initial_stats.new_effect.modify_attribute(
            object_list_unit_id=UnitInfo.HEAVY_DEMOLITION_SHIP.ID,
            source_player=PlayerId.EIGHT,
            object_attributes=ObjectAttribute.FOG_VISIBILITY,
            operation=Operation.SET,
            quantity=FogVisibility.ALWAYS_VISIBLE
        )

        initial_stats.new_effect.modify_attribute(
            object_list_unit_id=UnitInfo.HEAVY_DEMOLITION_SHIP.ID,
            source_player=PlayerId.EIGHT,
            object_attributes=ObjectAttribute.BLAST_WIDTH,
            operation=Operation.SET,
            quantity=3
        )

        initial_stats.new_effect.modify_attribute(
            object_list_unit_id=UnitInfo.HEAVY_DEMOLITION_SHIP.ID,
            source_player=PlayerId.EIGHT,
            object_attributes=ObjectAttribute.BLAST_WIDTH,
            operation=Operation.DIVIDE,
            quantity=2
        )

        initial_stats.new_effect.modify_attribute(
            object_list_unit_id=UnitInfo.HEAVY_DEMOLITION_SHIP.ID,
            source_player=PlayerId.EIGHT,
            object_attributes=ObjectAttribute.SEARCH_RADIUS,
            operation=Operation.SET,
            quantity=20
        )

        initial_stats.new_effect.modify_attribute(
            object_list_unit_id=UnitInfo.HEAVY_DEMOLITION_SHIP.ID,
            source_player=PlayerId.EIGHT,
            object_attributes=ObjectAttribute.SHOWN_ATTACK,
            operation=Operation.SET,
            quantity=1000
        )

    def demo_effects(self):
        damage_demo = self.trigger_manager.add_trigger("Fishing Area Demo", looping=True)

        damage_demo.new_effect.damage_object(
            object_list_unit_id=UnitInfo.HEAVY_DEMOLITION_SHIP.ID,
            source_player=PlayerId.EIGHT,
            area_x1=self.fishing_area.x1,
            area_y1=self.fishing_area.y1,
            area_x2=self.fishing_area.x2,
            area_y2=self.fishing_area.y2,
            quantity=5
        )

        damage_demo.new_effect.change_object_stance(
            object_list_unit_id=UnitInfo.HEAVY_DEMOLITION_SHIP.ID,
            source_player=PlayerId.EIGHT,
            area_x1=self.fishing_area.x1,
            area_y1=self.fishing_area.y1,
            area_x2=self.fishing_area.x2,
            area_y2=self.fishing_area.y2,
            attack_stance=AttackStance.AGGRESSIVE_STANCE
        )

    def spawn_demos(self):
        demo_checker = self.trigger_manager.add_trigger("Fishing Area Demo Checker", looping=True)

        demo_chance_timer1 = self.trigger_manager.add_trigger("Fishing Area Demo Chance Timer 1", enabled=False)
        demo_chance_timer2 = self.trigger_manager.add_trigger("Fishing Area Demo Chance Timer 2", enabled=False)
        demo_chance_timer3 = self.trigger_manager.add_trigger("Fishing Area Demo Chance Timer 3", enabled=False)
        demo_chance_timer4 = self.trigger_manager.add_trigger("Fishing Area Demo Chance Timer 4", enabled=False)

        demo_timer1 = self.trigger_manager.add_trigger("Fishing Area Demo Timer 1", enabled=False)
        demo_timer2 = self.trigger_manager.add_trigger("Fishing Area Demo Timer 2", enabled=False)
        demo_timer3 = self.trigger_manager.add_trigger("Fishing Area Demo Timer 3", enabled=False)
        demo_timer4 = self.trigger_manager.add_trigger("Fishing Area Demo Timer 4", enabled=False)

        demo_position1 = self.trigger_manager.add_trigger("Fishing Area Demo Position 1", enabled=False)
        demo_position2 = self.trigger_manager.add_trigger("Fishing Area Demo Position 2", enabled=False)
        demo_position3 = self.trigger_manager.add_trigger("Fishing Area Demo Position 3", enabled=False)
        demo_position4 = self.trigger_manager.add_trigger("Fishing Area Demo Position 4", enabled=False)

        # check if demo exists
        demo_checker.new_condition.own_fewer_objects(
            object_list=UnitInfo.HEAVY_DEMOLITION_SHIP.ID,
            source_player=PlayerId.EIGHT,
            area_x1=self.fishing_area.x1,
            area_y1=self.fishing_area.y1,
            area_x2=self.fishing_area.x2,
            area_y2=self.fishing_area.y2,
            quantity=0
        )
        demo_checker.new_effect.activate_trigger(trigger_id=demo_chance_timer1.trigger_id)
        demo_checker.new_effect.activate_trigger(trigger_id=demo_chance_timer2.trigger_id)
        demo_checker.new_effect.activate_trigger(trigger_id=demo_chance_timer3.trigger_id)
        demo_checker.new_effect.activate_trigger(trigger_id=demo_chance_timer4.trigger_id)
        demo_checker.new_effect.deactivate_trigger(trigger_id=demo_checker.trigger_id)

        # demo timer 1
        demo_chance_timer1.new_condition.chance(quantity=25)
        demo_chance_timer1.new_effect.activate_trigger(trigger_id=demo_timer1.trigger_id)
        demo_chance_timer1.new_effect.deactivate_trigger(trigger_id=demo_chance_timer1.trigger_id)
        demo_chance_timer1.new_effect.deactivate_trigger(trigger_id=demo_chance_timer2.trigger_id)
        demo_chance_timer1.new_effect.deactivate_trigger(trigger_id=demo_chance_timer3.trigger_id)
        demo_chance_timer1.new_effect.deactivate_trigger(trigger_id=demo_chance_timer4.trigger_id)

        # demo timer 2
        demo_chance_timer2.new_condition.chance(quantity=33)
        demo_chance_timer2.new_effect.activate_trigger(trigger_id=demo_timer2.trigger_id)
        demo_chance_timer2.new_effect.deactivate_trigger(trigger_id=demo_chance_timer1.trigger_id)
        demo_chance_timer2.new_effect.deactivate_trigger(trigger_id=demo_chance_timer2.trigger_id)
        demo_chance_timer2.new_effect.deactivate_trigger(trigger_id=demo_chance_timer3.trigger_id)
        demo_chance_timer2.new_effect.deactivate_trigger(trigger_id=demo_chance_timer4.trigger_id)

        # demo timer 3
        demo_chance_timer3.new_condition.chance(quantity=50)
        demo_chance_timer3.new_effect.activate_trigger(trigger_id=demo_timer3.trigger_id)
        demo_chance_timer3.new_effect.deactivate_trigger(trigger_id=demo_chance_timer1.trigger_id)
        demo_chance_timer3.new_effect.deactivate_trigger(trigger_id=demo_chance_timer2.trigger_id)
        demo_chance_timer3.new_effect.deactivate_trigger(trigger_id=demo_chance_timer3.trigger_id)
        demo_chance_timer3.new_effect.deactivate_trigger(trigger_id=demo_chance_timer4.trigger_id)

        # demo timer 4
        demo_chance_timer4.new_condition.chance(quantity=100)
        demo_chance_timer4.new_effect.activate_trigger(trigger_id=demo_timer4.trigger_id)
        demo_chance_timer4.new_effect.deactivate_trigger(trigger_id=demo_chance_timer1.trigger_id)
        demo_chance_timer4.new_effect.deactivate_trigger(trigger_id=demo_chance_timer2.trigger_id)
        demo_chance_timer4.new_effect.deactivate_trigger(trigger_id=demo_chance_timer3.trigger_id)
        demo_chance_timer4.new_effect.deactivate_trigger(trigger_id=demo_chance_timer4.trigger_id)

        demo_timer1.new_condition.timer(timer=12)
        demo_timer1.new_effect.activate_trigger(trigger_id=demo_position1.trigger_id)
        demo_timer1.new_effect.activate_trigger(trigger_id=demo_position2.trigger_id)
        demo_timer1.new_effect.activate_trigger(trigger_id=demo_position3.trigger_id)
        demo_timer1.new_effect.activate_trigger(trigger_id=demo_position4.trigger_id)

        demo_timer2.new_condition.timer(timer=16)
        demo_timer2.new_effect.activate_trigger(trigger_id=demo_position1.trigger_id)
        demo_timer2.new_effect.activate_trigger(trigger_id=demo_position2.trigger_id)
        demo_timer2.new_effect.activate_trigger(trigger_id=demo_position3.trigger_id)
        demo_timer2.new_effect.activate_trigger(trigger_id=demo_position4.trigger_id)

        demo_timer3.new_condition.timer(timer=20)
        demo_timer3.new_effect.activate_trigger(trigger_id=demo_position1.trigger_id)
        demo_timer3.new_effect.activate_trigger(trigger_id=demo_position2.trigger_id)
        demo_timer3.new_effect.activate_trigger(trigger_id=demo_position3.trigger_id)
        demo_timer3.new_effect.activate_trigger(trigger_id=demo_position4.trigger_id)

        demo_timer4.new_condition.timer(timer=24)
        demo_timer4.new_effect.activate_trigger(trigger_id=demo_position1.trigger_id)
        demo_timer4.new_effect.activate_trigger(trigger_id=demo_position2.trigger_id)
        demo_timer4.new_effect.activate_trigger(trigger_id=demo_position3.trigger_id)
        demo_timer4.new_effect.activate_trigger(trigger_id=demo_position4.trigger_id)

        # demo position 1
        demo_position1.new_condition.chance(quantity=25)
        demo_position1.new_effect.create_object(
            object_list_unit_id=UnitInfo.HEAVY_DEMOLITION_SHIP.ID,
            source_player=PlayerId.EIGHT,
            location_x=self.fishing_demo[0].x,
            location_y=self.fishing_demo[0].y
        )
        demo_position1.new_effect.change_object_attack(
            object_list_unit_id=UnitInfo.HEAVY_DEMOLITION_SHIP.ID,
            source_player=PlayerId.EIGHT,
            area_x1=self.fishing_demo[0].x,
            area_y1=self.fishing_demo[0].y,
            area_x2=self.fishing_demo[0].x,
            area_y2=self.fishing_demo[0].y,
            operation=Operation.SET,
            armour_attack_class=DamageClass.BASE_MELEE,
            armour_attack_quantity=1000
        )
        demo_position1.new_effect.deactivate_trigger(trigger_id=demo_position1.trigger_id)
        demo_position1.new_effect.deactivate_trigger(trigger_id=demo_position2.trigger_id)
        demo_position1.new_effect.deactivate_trigger(trigger_id=demo_position3.trigger_id)
        demo_position1.new_effect.deactivate_trigger(trigger_id=demo_position4.trigger_id)
        demo_position1.new_effect.activate_trigger(trigger_id=demo_checker.trigger_id)

        # demo position 2
        demo_position2.new_condition.chance(quantity=33)
        demo_position2.new_effect.create_object(
            object_list_unit_id=UnitInfo.HEAVY_DEMOLITION_SHIP.ID,
            source_player=PlayerId.EIGHT,
            location_x=self.fishing_demo[1].x,
            location_y=self.fishing_demo[1].y
        )
        demo_position2.new_effect.change_object_attack(
            object_list_unit_id=UnitInfo.HEAVY_DEMOLITION_SHIP.ID,
            source_player=PlayerId.EIGHT,
            area_x1=self.fishing_demo[1].x,
            area_y1=self.fishing_demo[1].y,
            area_x2=self.fishing_demo[1].x,
            area_y2=self.fishing_demo[1].y,
            operation=Operation.SET,
            armour_attack_class=DamageClass.BASE_MELEE,
            armour_attack_quantity=1000
        )
        demo_position2.new_effect.deactivate_trigger(trigger_id=demo_position1.trigger_id)
        demo_position2.new_effect.deactivate_trigger(trigger_id=demo_position2.trigger_id)
        demo_position2.new_effect.deactivate_trigger(trigger_id=demo_position3.trigger_id)
        demo_position2.new_effect.deactivate_trigger(trigger_id=demo_position4.trigger_id)
        demo_position2.new_effect.activate_trigger(trigger_id=demo_checker.trigger_id)

        # demo position 3
        demo_position3.new_condition.chance(quantity=50)
        demo_position3.new_effect.create_object(
            object_list_unit_id=UnitInfo.HEAVY_DEMOLITION_SHIP.ID,
            source_player=PlayerId.EIGHT,
            location_x=self.fishing_demo[2].x,
            location_y=self.fishing_demo[2].y
        )
        demo_position3.new_effect.change_object_attack(
            object_list_unit_id=UnitInfo.HEAVY_DEMOLITION_SHIP.ID,
            source_player=PlayerId.EIGHT,
            area_x1=self.fishing_demo[2].x,
            area_y1=self.fishing_demo[2].y,
            area_x2=self.fishing_demo[2].x,
            area_y2=self.fishing_demo[2].y,
            operation=Operation.SET,
            armour_attack_class=DamageClass.BASE_MELEE,
            armour_attack_quantity=1000
        )
        demo_position3.new_effect.deactivate_trigger(trigger_id=demo_position1.trigger_id)
        demo_position3.new_effect.deactivate_trigger(trigger_id=demo_position2.trigger_id)
        demo_position3.new_effect.deactivate_trigger(trigger_id=demo_position3.trigger_id)
        demo_position3.new_effect.deactivate_trigger(trigger_id=demo_position4.trigger_id)
        demo_position3.new_effect.activate_trigger(trigger_id=demo_checker.trigger_id)

        # demo position 4
        demo_position4.new_condition.chance(quantity=100)
        demo_position4.new_effect.create_object(
            object_list_unit_id=UnitInfo.HEAVY_DEMOLITION_SHIP.ID,
            source_player=PlayerId.EIGHT,
            location_x=self.fishing_demo[3].x,
            location_y=self.fishing_demo[3].y
        )
        demo_position4.new_effect.change_object_attack(
            object_list_unit_id=UnitInfo.HEAVY_DEMOLITION_SHIP.ID,
            source_player=PlayerId.EIGHT,
            area_x1=self.fishing_demo[3].x,
            area_y1=self.fishing_demo[3].y,
            area_x2=self.fishing_demo[3].x,
            area_y2=self.fishing_demo[3].y,
            operation=Operation.SET,
            armour_attack_class=DamageClass.BASE_MELEE,
            armour_attack_quantity=1000
        )
        demo_position4.new_effect.deactivate_trigger(trigger_id=demo_position1.trigger_id)
        demo_position4.new_effect.deactivate_trigger(trigger_id=demo_position2.trigger_id)
        demo_position4.new_effect.deactivate_trigger(trigger_id=demo_position3.trigger_id)
        demo_position4.new_effect.deactivate_trigger(trigger_id=demo_position4.trigger_id)
        demo_position4.new_effect.activate_trigger(trigger_id=demo_checker.trigger_id)


