import math

from AoE2ScenarioParser.datasets.other import OtherInfo
from AoE2ScenarioParser.datasets.players import PlayerId
from AoE2ScenarioParser.datasets.trigger_lists import Operation, ObjectAttribute, AttackStance, TerrainRestrictions, ObjectState
from AoE2ScenarioParser.datasets.units import UnitInfo
from AoE2ScenarioParser.objects.support.area import Area

from scenarios.lib.parser_project import ParserProject
from scenarios.lib.civ_settings import CivSettings
from scenarios.lib.unit_modifier import UnitModifier


class MazeRunner(ParserProject):
    MOVEABLE_TREE = OtherInfo.TREE_OAK_AUTUMN_SNOW.ID
    LEOPARD = UnitInfo.SNOW_LEOPARD.ID
    NORMAL_TREE = OtherInfo.TREE_PINE_FOREST.ID

    def __init__(self, input_scenario_name: str, output_scenario_name: str):
        super().__init__(input_scenario_name, output_scenario_name)
        self.player_list = [PlayerId.ONE, PlayerId.TWO]
        self.trigger_manager = self.scenario.trigger_manager
        self.data_triggers = self.scenario.actions.load_data_triggers()
        self.leopard_speed = 2
        self.g1_entrance_delay = 300
        self.interior_delay = 600
        self.clearing_delay = 900
        self.way_delay = 300
        self.sound = 'tree_roots'

    def process(self):
        CivSettings(self.scenario, self.player_list)
        self.stats()
        first_way_list, second_way_list = [], []
        for i, (key, areas) in enumerate(self.data_triggers.areas.items()):
            first_way = self.move_trees(areas[0], areas[1])
            second_way = self.move_trees(areas[1], areas[0])
            first_way.new_effect.activate_trigger(second_way.trigger_id)
            second_way.new_effect.activate_trigger(first_way.trigger_id)
            first_way_list.append(first_way)
            second_way_list.append(second_way)

        g1_delay = self.trigger_manager.add_trigger('G1 Delay', enabled=True)
        g1_entrance = self.trigger_manager.add_trigger('G1 Entrance', enabled=False)
        g1_entrance_negative = self.trigger_manager.add_trigger('G1 Entrance Negative', enabled=False)

        g2_sideways = self.trigger_manager.add_trigger('G2 Sideways', enabled=False)
        g3_sideways = self.trigger_manager.add_trigger('G3 Sideways', enabled=False)

        interior_1_delay = self.trigger_manager.add_trigger("Interior 1 Delay", enabled=True)
        interior_1 = self.trigger_manager.add_trigger("Interior 1", enabled=False)
        interior_1_negative = self.trigger_manager.add_trigger("Interior 1 Negative", enabled=False)

        central_clearing_delay = self.trigger_manager.add_trigger("Central Clearing Delay", enabled=True)
        central_clearing = self.trigger_manager.add_trigger("Central Clearing", enabled=False)
        central_clearing_negative = self.trigger_manager.add_trigger("Central Clearing Negative", enabled=False)

        g1_delay.new_condition.timer(self.g1_entrance_delay)
        g1_delay.new_effect.activate_trigger(g1_entrance.trigger_id)
        g1_delay.new_effect.activate_trigger(g1_entrance_negative.trigger_id)
        g1_entrance.new_condition.chance(50)
        g1_entrance.new_effect.activate_trigger(first_way_list[0].trigger_id)
        g1_entrance.new_effect.activate_trigger(first_way_list[1].trigger_id)
        g1_entrance.new_effect.deactivate_trigger(g1_entrance_negative.trigger_id)
        g1_entrance.new_effect.activate_trigger(g2_sideways.trigger_id)
        g1_entrance.new_effect.activate_trigger(g3_sideways.trigger_id)
        g1_entrance_negative.new_effect.deactivate_trigger(g1_entrance.trigger_id)

        g2_sideways.new_condition.chance(50)
        g2_sideways.new_effect.activate_trigger(first_way_list[2].trigger_id)
        g2_sideways.new_effect.activate_trigger(first_way_list[3].trigger_id)
        g2_sideways.new_effect.deactivate_trigger(g3_sideways.trigger_id)

        g3_sideways.new_effect.activate_trigger(first_way_list[4].trigger_id)
        g3_sideways.new_effect.activate_trigger(first_way_list[5].trigger_id)
        g3_sideways.new_effect.deactivate_trigger(g2_sideways.trigger_id)

        interior_1_delay.new_condition.timer(self.interior_delay)
        interior_1_delay.new_effect.activate_trigger(interior_1.trigger_id)
        interior_1_delay.new_effect.activate_trigger(interior_1_negative.trigger_id)
        interior_1.new_condition.chance(50)
        interior_1.new_effect.activate_trigger(first_way_list[6].trigger_id)
        interior_1.new_effect.activate_trigger(first_way_list[7].trigger_id)
        interior_1.new_effect.activate_trigger(first_way_list[8].trigger_id)
        interior_1.new_effect.deactivate_trigger(interior_1_negative.trigger_id)
        interior_1_negative.new_effect.deactivate_trigger(interior_1.trigger_id)

        central_clearing_delay.new_condition.timer(self.clearing_delay)
        central_clearing_delay.new_effect.activate_trigger(central_clearing.trigger_id)
        central_clearing_delay.new_effect.activate_trigger(central_clearing_negative.trigger_id)
        central_clearing.new_condition.chance(50)
        central_clearing.new_effect.activate_trigger(first_way_list[9].trigger_id)
        central_clearing.new_effect.activate_trigger(first_way_list[10].trigger_id)
        central_clearing.new_effect.activate_trigger(first_way_list[11].trigger_id)
        central_clearing.new_effect.activate_trigger(first_way_list[12].trigger_id)
        central_clearing.new_effect.deactivate_trigger(central_clearing_negative.trigger_id)
        central_clearing_negative.new_effect.deactivate_trigger(central_clearing.trigger_id)

    def stats(self):
        initial_replace = self.trigger_manager.add_trigger('Initial Replace')
        initial_replace.new_condition.timer(2)
        initial_replace.new_effect.replace_object(
            source_player=PlayerId.GAIA,
            target_player=PlayerId.GAIA,
            object_list_unit_id=self.MOVEABLE_TREE,
            object_list_unit_id_2=self.LEOPARD,
        )
        initial_replace.new_effect.replace_object(
            source_player=PlayerId.GAIA,
            target_player=PlayerId.GAIA,
            object_list_unit_id=self.LEOPARD,
            object_list_unit_id_2=self.MOVEABLE_TREE,
        )
        (UnitModifier(self.scenario, self.MOVEABLE_TREE, PlayerId.GAIA)
         .modify_attribute(ObjectAttribute.DEAD_UNIT_ID, Operation.SET, self.MOVEABLE_TREE)
         .modify_attribute(ObjectAttribute.TERRAIN_RESTRICTION_ID, Operation.SET, TerrainRestrictions.ALL)
         .modify_attribute(ObjectAttribute.STANDING_GRAPHIC, Operation.SET, 2310)
         .modify_attribute(ObjectAttribute.OBJECT_NAME_ID, Operation.SET, 5399)
         .create_triggers())
        (UnitModifier(self.scenario, self.NORMAL_TREE, PlayerId.GAIA)
         .modify_attribute(ObjectAttribute.DEAD_UNIT_ID, Operation.SET, self.NORMAL_TREE)
         .create_triggers())
        (UnitModifier(self.scenario, UnitInfo.SNOW_LEOPARD.ID, PlayerId.GAIA)
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
    maze_runner = MazeRunner(
        input_scenario_name='CORREDOR_DEL_LABERINTO',
        output_scenario_name='CORREDOR_DEL_LABERINTO_output'
    )
    maze_runner.convert()
