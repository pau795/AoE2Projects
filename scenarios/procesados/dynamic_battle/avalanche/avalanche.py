import math
from operator import add

from AoE2ScenarioParser.datasets.other import OtherInfo
from AoE2ScenarioParser.datasets.players import PlayerId
from AoE2ScenarioParser.datasets.trigger_lists import ActionType, ObjectAttribute, Operation, AttackStance, CombatAbility, OcclusionMode
from AoE2ScenarioParser.datasets.units import UnitInfo
from AoE2ScenarioParser.objects.support.area import Area
from AoE2ScenarioParser.objects.support.tile import Tile
from scenarios.lib.parser_project import ParserProject
from scenarios.lib.unit_modifier import UnitModifier
from scenarios.lib.xs.unit_tasks import MovementDamageTask, TaskTargets


class Avalanche(ParserProject):
    FLAG_LIST = [OtherInfo.FLAG_A.ID, OtherInfo.FLAG_B.ID, OtherInfo.FLAG_C.ID, OtherInfo.FLAG_D.ID]
    PREDATOR_LIST = [UnitInfo.BLACK_PANTHER.ID, UnitInfo.BLACK_BEAR.ID, UnitInfo.JAGUAR.ID, UnitInfo.TIGER.ID]

    def __init__(self, input_scenario_name: str, output_scenario_name: str):
        super().__init__(input_scenario_name, output_scenario_name)
        self.trigger_manager = self.scenario.trigger_manager
        self.map_manager = self.scenario.map_manager
        self.unit_manager = self.scenario.unit_manager
        self.xs_manager = self.scenario.xs_manager
        self.data_triggers = self.scenario.actions.load_data_triggers()

    def generate_avalanches(self, corner_tile: Tile, avalanche_areas: list[Area]):
        triggers = []
        for area in avalanche_areas:
            unit_list = self.unit_manager.get_units_in_area(
                x1=area.x1,
                y1=area.y1,
                x2=area.x2,
                y2=area.y2
            )
            replace_trigger = self.trigger_manager.add_trigger("Replace Flags", enabled=False)
            avalanche_trigger = self.trigger_manager.add_trigger("Avalanche", enabled=False)
            for flag_unit, predator_unit in zip(self.FLAG_LIST, self.PREDATOR_LIST):
                replace_trigger.new_effect.kill_object(
                    object_list_unit_id=flag_unit,
                    source_player=PlayerId.GAIA,
                    area_x1=area.x1,
                    area_y1=area.y1,
                    area_x2=area.x2,
                    area_y2=area.y2,
                )
                replace_trigger.new_effect.disable_unit_targeting(
                    object_list_unit_id=predator_unit,
                    source_player=PlayerId.GAIA,
                    area_x1=area.x1,
                    area_y1=area.y1,
                    area_x2=area.x2,
                    area_y2=area.y2,
                )
                replace_trigger.new_effect.disable_object_selection(
                    object_list_unit_id=predator_unit,
                    source_player=PlayerId.GAIA,
                    area_x1=area.x1,
                    area_y1=area.y1,
                    area_x2=area.x2,
                    area_y2=area.y2,
                )
                replace_trigger.new_effect.change_object_stance(
                    object_list_unit_id=predator_unit,
                    source_player=PlayerId.GAIA,
                    area_x1=area.x1,
                    area_y1=area.y1,
                    area_x2=area.x2,
                    area_y2=area.y2,
                    attack_stance=AttackStance.NO_ATTACK_STANCE
                )
                replace_trigger.new_effect.activate_trigger(avalanche_trigger.trigger_id)
                avalanche_trigger.new_condition.timer(3)
            for unit in [x for x in unit_list if x.unit_const in self.FLAG_LIST]:
                vector = [unit.x - (corner_tile.x + 0.5), unit.y - (corner_tile.y + 0.5)]
                distance = (math.sqrt(vector[0] ** 2 + vector[1] ** 2))
                normal_vector = (vector[0] / distance, vector[1] / distance)
                x, y = unit.x, unit.y
                while 0 <= x < self.map_manager.map_width and 0 <= y < self.map_manager.map_height:
                    x += normal_vector[0]
                    y += normal_vector[1]
                x = int(x - normal_vector[0])
                y = int(y - normal_vector[1])

                avalanche_trigger.new_effect.task_object(
                    area_x1=int(unit.x),
                    area_y1=int(unit.y),
                    area_x2=int(unit.x),
                    area_y2=int(unit.y),
                    source_player=PlayerId.GAIA,
                    location_x=x,
                    location_y=y,
                    action_type=ActionType.MOVE
                )
            triggers.append(replace_trigger)
        return triggers

    def unit_stats(self):
        graphic_dict = {
            UnitInfo.BLACK_PANTHER.ID: 10642,
            UnitInfo.BLACK_BEAR.ID: 10641,
            UnitInfo.JAGUAR.ID: 10640,
            UnitInfo.TIGER.ID: 10639
        }
        (UnitModifier(self.scenario, OtherInfo.FLAG_E.ID, PlayerId.GAIA)
         .modify_attribute(ObjectAttribute.STANDING_GRAPHIC, Operation.SET, 10644)
         .create_triggers()
         )
        snowball_acceleration_trigger = self.trigger_manager.add_trigger("Snowball Acceleration", looping=True)
        for unit_id, graphic_id in graphic_dict.items():
            (UnitModifier(self.scenario, unit_id, PlayerId.GAIA)
             .modify_attribute(ObjectAttribute.HIT_POINTS, Operation.SET, 20000)
             .modify_attribute(ObjectAttribute.UNIT_SIZE_X, Operation.SET, 0)
             .modify_attribute(ObjectAttribute.UNIT_SIZE_Y, Operation.SET, 0)
             .modify_attribute(ObjectAttribute.UNIT_SIZE_Z, Operation.SET, 0)
             .modify_attribute(ObjectAttribute.OCCLUSION_MODE, Operation.SET, OcclusionMode.DISPLAY_OUTLINE)
             .modify_attribute(ObjectAttribute.STANDING_GRAPHIC, Operation.SET, 10638)
             .modify_attribute(ObjectAttribute.WALKING_GRAPHIC, Operation.SET, graphic_id)
             .modify_attribute(ObjectAttribute.ATTACK_GRAPHIC, Operation.SET, graphic_id)
             .modify_attribute(ObjectAttribute.DYING_GRAPHIC, Operation.SET, -1)
             .modify_attribute(ObjectAttribute.DEAD_UNIT_ID, Operation.SET, -1)
             .modify_attribute(ObjectAttribute.FOG_VISIBILITY, Operation.SET, 1)
             .modify_attribute(ObjectAttribute.TERRAIN_RESTRICTION_ID, Operation.SET, 41)
             .modify_attribute(ObjectAttribute.MOVEMENT_SPEED, Operation.SET, 1.2)
             .add_task(MovementDamageTask(
                damage_per_tick=50,
                tick_interval_seconds=1,
                effect_range=0.5
             ))
             .create_triggers()
             )
            snowball_acceleration_trigger.new_condition.timer(3)
            snowball_acceleration_trigger.new_effect.modify_object_attribute(
                object_list_unit_id=unit_id,
                source_player=PlayerId.GAIA,
                object_attributes=ObjectAttribute.MOVEMENT_SPEED,
                operation=Operation.ADD,
                quantity=0.10
            )

        for flag_id, predator_id in zip(self.FLAG_LIST, self.PREDATOR_LIST):
            (UnitModifier(self.scenario, flag_id, PlayerId.GAIA)
             .modify_attribute(ObjectAttribute.STANDING_GRAPHIC, Operation.SET, 0)
             .modify_attribute(ObjectAttribute.DEAD_UNIT_ID, Operation.SET, predator_id)
             .create_triggers()
             )

    def process(self):
        self.xs_manager.initialise_xs_trigger()
        self.unit_stats()
        top_corner_tile = self.data_triggers.tiles['top_corner'][0]
        top_corner_areas = self.data_triggers.areas['top_flags']
        top_triggers = self.generate_avalanches(top_corner_tile, top_corner_areas)

        enable_middle = self.trigger_manager.add_trigger("enable_middle")
        enable_middle.new_condition.timer(15)
        enable_middle.new_effect.create_object(
            object_list_unit_id=OtherInfo.FLAG_E.ID,
            source_player=PlayerId.GAIA,
            location_x=top_corner_tile.x,
            location_y=top_corner_tile.y,
        )
        enable_middle.new_effect.activate_trigger(top_triggers[0].trigger_id)
        enable_middle.new_effect.activate_trigger(top_triggers[1].trigger_id)
        enable_middle.new_effect.activate_trigger(top_triggers[2].trigger_id)


if __name__ == '__main__':
    avalanche_class = Avalanche(
        input_scenario_name=f'EDIT_AVALANCHE_1V1',
        output_scenario_name=f'OUTPUT_AVALANCHE_1V1',
    )
    avalanche_class.convert()
