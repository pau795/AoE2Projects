from AoE2ScenarioParser.datasets.players import PlayerId
from AoE2ScenarioParser.datasets.trigger_lists import ObjectAttribute, Operation, AttackStance
from AoE2ScenarioParser.datasets.units import UnitInfo
from AoE2ScenarioParser.objects.managers.trigger_manager import TriggerManager
from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario
from AoE2ScenarioParser.scenarios.support.data_triggers import DataTriggers


class HuntingArea:

    def __init__(self, scenario: AoE2DEScenario, trigger_data: DataTriggers):
        self.trigger_manager: TriggerManager = scenario.trigger_manager
        self.trigger_data = trigger_data
        self.deer_spawn_tile = self.trigger_data.tiles['hunting_deer'][0]
        self.entire_hunting_area = self.trigger_data.areas['hunting_deer'][0]
        self.deer_death_area = self.trigger_data.areas['hunting_deer'][1]
        self.hunting_pass = self.trigger_data.areas['hunting_pass']
        self.hunting_units = self.trigger_data.areas['hunting_units']
        self.init_attributes()
        self.deer()

    def init_attributes(self):
        init_attributes = self.trigger_manager.add_trigger('Hunting Area Initial Attributes')

        for units_area in self.hunting_units:
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

    def deer(self):
        deer_hp = self.trigger_manager.add_trigger("Hunting Area Deer HP")
        deer_spawn = self.trigger_manager.add_trigger("Hunting Area Spawn Deer", looping=True)
        deer_death = self.trigger_manager.add_trigger("Hunting Area Deer Death", looping=True)
        deer_remove = self.trigger_manager.add_trigger("Hunting Area Deer Remove", looping=True)

        deer_hp.new_effect.modify_attribute(
            object_list_unit_id=UnitInfo.DEER.ID,
            source_player=PlayerId.GAIA,
            object_attributes=ObjectAttribute.HIT_POINTS,
            operation=Operation.SET,
            quantity=20000)

        deer_spawn.new_condition.own_fewer_objects(
            object_list=UnitInfo.DEER.ID,
            source_player=PlayerId.GAIA,
            area_x1=self.entire_hunting_area.x1,
            area_y1=self.entire_hunting_area.y1,
            area_x2=self.entire_hunting_area.x2,
            area_y2=self.entire_hunting_area.y2,
            quantity=1
        )

        deer_spawn.new_effect.create_object(
            object_list_unit_id=UnitInfo.DEER.ID,
            source_player=PlayerId.GAIA,
            location_x=self.deer_spawn_tile.x,
            location_y=self.deer_spawn_tile.y
        )

        deer_death.new_effect.kill_object(
            object_list_unit_id=UnitInfo.DEER.ID,
            source_player=PlayerId.GAIA,
            area_x1=self.deer_death_area.x1,
            area_y1=self.deer_death_area.y1,
            area_x2=self.deer_death_area.x2,
            area_y2=self.deer_death_area.y2,
        )

        deer_remove.new_effect.remove_object(
            object_list_unit_id=UnitInfo.DEER.ID,
            source_player=PlayerId.GAIA,
            area_x1=self.hunting_pass[0].x1,
            area_x2=self.hunting_pass[0].x2,
            area_y2=self.hunting_pass[0].y2,
            area_y1=self.hunting_pass[0].y1,
        )


