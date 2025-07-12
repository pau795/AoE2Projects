import math

from AoE2ScenarioParser.datasets.other import OtherInfo
from AoE2ScenarioParser.datasets.players import PlayerId
from AoE2ScenarioParser.datasets.trigger_lists import Operation, ObjectAttribute, AttackStance, TerrainRestrictions, ObjectState
from AoE2ScenarioParser.datasets.units import UnitInfo
from AoE2ScenarioParser.objects.support.area import Area

from scenarios.lib.parser_project import ParserProject
from scenarios.lib.civ_settings import CivSettings
from scenarios.lib.unit_modifier import UnitModifier


class BosqueEncantadoMultiplayer(ParserProject):
    LEOPARD = UnitInfo.SNOW_LEOPARD.ID
    MOVEABLE_TREE = OtherInfo.TREE_PINE_FOREST.ID

    def __init__(self, input_scenario_name: str, output_scenario_name: str):
        super().__init__(input_scenario_name, output_scenario_name)
        self.trigger_manager = self.scenario.trigger_manager
        self.data_triggers = self.scenario.actions.load_data_triggers()
        self.leopard_speed = 2
        self.forest_delay = 300
        self.way_delay = 300
        self.player_list = [PlayerId.ONE, PlayerId.TWO, PlayerId.THREE, PlayerId.FOUR]
        self.sound = 'tree_roots'

    @staticmethod
    def calculate_delay(i):
        if 0 < i <= 4:
            return 300
        elif 4 < i <= 8:
            return 500
        elif 12 < i <= 24:
            return 750
        elif 8 < i <= 12:
            return 1000
        else:
            return 1

    def process(self):
        CivSettings(self.scenario, self.player_list)
        self.stats()
        for i, (key, areas) in enumerate(self.data_triggers.areas.items()):
            first_way = self.move_trees(areas[0], areas[1])
            second_way = self.move_trees(areas[1], areas[0])
            first_way.new_effect.activate_trigger(second_way.trigger_id)
            second_way.new_effect.activate_trigger(first_way.trigger_id)
            initial_forest_delay = self.trigger_manager.add_trigger(f'{key} initial forest delay', enabled=True)
            initial_forest_delay.new_condition.timer(self.calculate_delay(i + 1))
            initial_forest_delay.new_effect.activate_trigger(first_way.trigger_id)

    def stats(self):
        (UnitModifier(self.scenario, OtherInfo.TREE_PINE_FOREST.ID, PlayerId.GAIA)
         .modify_attribute(ObjectAttribute.DEAD_UNIT_ID, Operation.SET, OtherInfo.TREE_PINE_FOREST.ID)
         .create_triggers())
        (UnitModifier(self.scenario, UnitInfo.SNOW_LEOPARD.ID, PlayerId.GAIA)
         .modify_attribute(ObjectAttribute.HIT_POINTS, Operation.SET, 20000)
         .modify_attribute(ObjectAttribute.UNIT_SIZE_X, Operation.SET, 0)
         .modify_attribute(ObjectAttribute.UNIT_SIZE_Y, Operation.SET, 0)
         .modify_attribute(ObjectAttribute.UNIT_SIZE_Z, Operation.SET, 0)
         .modify_attribute(ObjectAttribute.TERRAIN_RESTRICTION_ID, Operation.SET, TerrainRestrictions.ALL)
         .modify_attribute(ObjectAttribute.MOVEMENT_SPEED, Operation.SET, self.leopard_speed)
         .modify_attribute(ObjectAttribute.ATTACK, Operation.SET, 0, 4)
         .modify_attribute(ObjectAttribute.SHOWN_ATTACK, Operation.SET, 0)
         .modify_attribute(ObjectAttribute.STANDING_GRAPHIC, Operation.SET, 2310)
         .modify_attribute(ObjectAttribute.WALKING_GRAPHIC, Operation.SET, 2310)
         .modify_attribute(ObjectAttribute.ICON_ID, Operation.SET, OtherInfo.TREE_PINE_FOREST.ICON_ID)
         .modify_attribute(ObjectAttribute.OBJECT_NAME_ID, Operation.SET, 5399)
         .create_triggers())

    def move_trees(self, source_area: Area, target_area: Area):
        source_tiles = source_area.to_coords()
        target_tiles = target_area.to_coords()
        trees_phase_1 = self.trigger_manager.add_trigger(f"Remove Trees, Create Leopards, Move Leopards", enabled=False)
        trees_phase_2 = self.trigger_manager.add_trigger(f"Check for Leopards, Remove Leopards, Create Trees", enabled=False)
        trees_phase_1.new_condition.timer(self.way_delay)
        trees_phase_1.new_effect.remove_object(
            object_list_unit_id=self.MOVEABLE_TREE,
            source_player=PlayerId.GAIA,
            object_state=ObjectState.ALIVE,
            area_x1=source_area.x1,
            area_y1=source_area.y1,
            area_x2=source_area.x2,
            area_y2=source_area.y2
        )
        trees_phase_1.new_effect.remove_object(
            object_list_unit_id=self.MOVEABLE_TREE,
            source_player=PlayerId.GAIA,
            object_state=ObjectState.RESOURCE,
            area_x1=source_area.x1,
            area_y1=source_area.y1,
            area_x2=source_area.x2,
            area_y2=source_area.y2
        )
        for source_tile in source_tiles:
            trees_phase_1.new_effect.create_object(
                object_list_unit_id=self.LEOPARD,
                source_player=PlayerId.GAIA,
                location_x=source_tile.x,
                location_y=source_tile.y
            )
        trees_phase_1.new_effect.change_object_stance(
            object_list_unit_id=self.LEOPARD,
            source_player=PlayerId.GAIA,
            area_x1=source_area.x1,
            area_y1=source_area.y1,
            area_x2=source_area.x2,
            area_y2=source_area.y2,
            attack_stance=AttackStance.NO_ATTACK_STANCE
        )

        trees_phase_1.new_effect.disable_object_selection(
            object_list_unit_id=self.LEOPARD,
            source_player=PlayerId.GAIA,
            area_x1=source_area.x1,
            area_y1=source_area.y1,
            area_x2=source_area.x2,
            area_y2=source_area.y2
        )
        trees_phase_1.new_effect.disable_unit_targeting(
            object_list_unit_id=self.LEOPARD,
            source_player=PlayerId.GAIA,
            area_x1=source_area.x1,
            area_y1=source_area.y1,
            area_x2=source_area.x2,
            area_y2=source_area.y2
        )
        for i, source_tile in enumerate(source_tiles):
            trees_phase_1.new_effect.task_object(
                object_list_unit_id=UnitInfo.SNOW_LEOPARD.ID,
                source_player=PlayerId.GAIA,
                area_x1=source_tile.x,
                area_y1=source_tile.y,
                area_x2=source_tile.x,
                area_y2=source_tile.y,
                location_x=target_tiles[i].x,
                location_y=target_tiles[i].y
            )
        for player in self.player_list:
            trees_phase_1.new_effect.play_sound(
                sound_name=self.sound,
                source_player=player,
                location_x=int(source_area.get_center()[0]),
                location_y=int(source_area.get_center()[1])

            )
        trees_phase_1.new_effect.activate_trigger(trigger_id=trees_phase_2.trigger_id)

        # PHASE 2
        distance = math.dist(source_area.get_center(), target_area.get_center())
        rotation = source_area.get_width() != target_area.get_width()
        timer = int(math.ceil(distance / self.leopard_speed) + (4 * (2 if rotation else 1))) + 1
        trees_phase_2.new_condition.timer(timer=timer)

        trees_phase_2.new_effect.remove_object(
            object_list_unit_id=self.LEOPARD,
            source_player=PlayerId.GAIA,
            object_state=ObjectState.ALIVE,
            area_x1=max(0, target_area.x1 - 1),
            area_y1=max(0, target_area.y1 - 1),
            area_x2=min(self.scenario.map_manager.map_width - 1, target_area.x2 + 1),
            area_y2=min(self.scenario.map_manager.map_height - 1, target_area.y2 + 1)
        )
        for player in self.player_list:
            trees_phase_2.new_effect.kill_object(
                source_player=player,
                area_x1=max(0, target_area.x1 - 1),
                area_y1=max(0, target_area.y1 - 1),
                area_x2=min(self.scenario.map_manager.map_width - 1, target_area.x2 + 1),
                area_y2=min(self.scenario.map_manager.map_height - 1, target_area.y2 + 1)
            )
        for target_tile in target_tiles:
            trees_phase_2.new_effect.create_object(
                object_list_unit_id=self.LEOPARD,
                source_player=PlayerId.GAIA,
                location_x=target_tile.x,
                location_y=target_tile.y
            )
        trees_phase_2.new_effect.replace_object(
            object_list_unit_id=self.LEOPARD,
            object_list_unit_id_2=self.MOVEABLE_TREE,
            source_player=PlayerId.GAIA,
            target_player=PlayerId.GAIA,
            area_x1=max(0, target_area.x1 - 1),
            area_y1=max(0, target_area.y1 - 1),
            area_x2=min(self.scenario.map_manager.map_width - 1, target_area.x2 + 1),
            area_y2=min(self.scenario.map_manager.map_height - 1, target_area.y2 + 1)
        )
        return trees_phase_1


if __name__ == '__main__':
    bosque_encantado_class = BosqueEncantadoMultiplayer(
        input_scenario_name='EDIT_ENCHANTED_FOREST_2V2',
        output_scenario_name='OUTPUT_ENCHANTED_FOREST_2V2'
    )
    bosque_encantado_class.convert()
