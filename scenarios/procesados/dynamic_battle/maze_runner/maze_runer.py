import math

from AoE2ScenarioParser.datasets.buildings import BuildingInfo
from AoE2ScenarioParser.datasets.other import OtherInfo
from AoE2ScenarioParser.datasets.players import PlayerId
from AoE2ScenarioParser.datasets.terrains import TerrainId
from AoE2ScenarioParser.datasets.trigger_lists import Operation, ObjectAttribute, AttackStance, TerrainRestrictions, ObjectState
from AoE2ScenarioParser.datasets.units import UnitInfo
from AoE2ScenarioParser.objects.data_objects.trigger import Trigger
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
        self.block1_period = 300
        self.block2_period = 600
        self.block3_period = 300
        self.sound = 'tree_roots'
        self.debug_messages = False
        self.remove_revealer_trigger = self.trigger_manager.add_trigger('Remove Revealer')

    def process(self):
        CivSettings(self.scenario, self.player_list)
        self.stats()
        self.remove_revealer_trigger.new_condition.timer(2)
        for player in self.player_list:
            self.remove_revealer_trigger.new_effect.remove_object(
                object_list_unit_id=OtherInfo.MAP_REVEALER.ID,
                source_player=player,
            )
        movement_list: list[tuple[Trigger, Trigger]] = []

        for i, (key, areas) in enumerate(self.data_triggers.areas.items()):
            print(i, key)
            first_way = self.move_trees(i, areas[0], areas[1], False)
            second_way = self.move_trees(i, areas[1], areas[0], True)
            movement_list.append((first_way, second_way))

        g1_node = self.trigger_manager.add_trigger('G1 Node', enabled=True, looping=False)
        g1_node_chance = self.trigger_manager.add_trigger('G1 Chance', enabled=False)
        g1_node_chance_negative = self.trigger_manager.add_trigger('G1 Chance Negative', enabled=False)

        g1_left_side_chance = self.trigger_manager.add_trigger('G2 Left Side Chance', enabled=False)
        g1_right_side_chance = self.trigger_manager.add_trigger('G2 Right Side Chance', enabled=False)

        g1_left_side_node = self.trigger_manager.add_trigger('G1 Left Side Node', enabled=False, looping=False)
        g1_left_side_node_chance = self.trigger_manager.add_trigger('G1 Left Side Node Chance', enabled=False, looping=False)
        g1_left_side_node_chance_negative = self.trigger_manager.add_trigger('G2 Left Side Node Chance Negative', enabled=False, looping=False)

        g1_right_side_node = self.trigger_manager.add_trigger('G2 Right Side Node', enabled=False, looping=False)
        g1_right_side_node_chance = self.trigger_manager.add_trigger('G2 Right Side Node Chance', enabled=False, looping=False)
        g1_right_side_node_chance_negative = self.trigger_manager.add_trigger('G2 Right Side Node Chance Negative', enabled=False, looping=False)

        g1_node.new_condition.timer(self.block1_period)
        g1_node.new_effect.activate_trigger(g1_node_chance.trigger_id)
        g1_node.new_effect.activate_trigger(g1_node_chance_negative.trigger_id)

        g1_node_chance.new_condition.chance(50)
        # ACTUAL MOVEMENT TRIGGER
        g1_node_chance.new_effect.activate_trigger(movement_list[0][0].trigger_id)
        g1_node_chance.new_effect.activate_trigger(movement_list[1][0].trigger_id)
        if self.debug_messages:
            g1_node_chance.new_effect.send_chat(message=f"G1 Node Chance")
        # ARCS
        g1_node_chance.new_effect.activate_trigger(g1_left_side_chance.trigger_id)
        g1_node_chance.new_effect.activate_trigger(g1_right_side_chance.trigger_id)
        g1_node_chance.new_effect.deactivate_trigger(g1_node_chance_negative.trigger_id)

        # NEGATIVE NODE
        g1_node_chance_negative.new_effect.activate_trigger(g1_node.trigger_id)
        g1_node_chance_negative.new_effect.deactivate_trigger(g1_node_chance.trigger_id)
        if self.debug_messages:
            g1_node_chance_negative.new_effect.send_chat(message=f"G1 Node Chance Negative")

        # CHOICES
        g1_left_side_chance.new_condition.chance(50)
        g1_left_side_chance.new_effect.activate_trigger(movement_list[2][0].trigger_id)
        g1_left_side_chance.new_effect.activate_trigger(movement_list[3][0].trigger_id)
        if self.debug_messages:
            g1_left_side_chance.new_effect.send_chat(message=f"G1 Left Side Chance")
        g1_left_side_chance.new_effect.activate_trigger(g1_left_side_node.trigger_id)
        g1_left_side_chance.new_effect.deactivate_trigger(g1_left_side_chance.trigger_id)
        g1_left_side_chance.new_effect.deactivate_trigger(g1_right_side_chance.trigger_id)

        g1_right_side_chance.new_condition.chance(100)
        g1_right_side_chance.new_effect.activate_trigger(movement_list[4][0].trigger_id)
        g1_right_side_chance.new_effect.activate_trigger(movement_list[5][0].trigger_id)
        if self.debug_messages:
            g1_right_side_chance.new_effect.send_chat(message=f"G1 Right Side Chance")
        g1_right_side_chance.new_effect.activate_trigger(g1_right_side_node.trigger_id)
        g1_right_side_chance.new_effect.deactivate_trigger(g1_left_side_chance.trigger_id)
        g1_right_side_chance.new_effect.deactivate_trigger(g1_right_side_chance.trigger_id)

        # LEFT RETURN
        g1_left_side_node.new_condition.timer(self.block1_period)
        g1_left_side_node.new_effect.activate_trigger(g1_left_side_node_chance.trigger_id)
        g1_left_side_node.new_effect.activate_trigger(g1_left_side_node_chance_negative.trigger_id)

        g1_left_side_node_chance.new_condition.chance(50)
        g1_left_side_node_chance.new_effect.activate_trigger(movement_list[0][1].trigger_id)
        g1_left_side_node_chance.new_effect.activate_trigger(movement_list[1][1].trigger_id)
        g1_left_side_node_chance.new_effect.activate_trigger(movement_list[2][1].trigger_id)
        g1_left_side_node_chance.new_effect.activate_trigger(movement_list[3][1].trigger_id)
        if self.debug_messages:
            g1_left_side_node_chance.new_effect.send_chat(message=f"G1 Left Side Node Chance")
        g1_left_side_node_chance.new_effect.activate_trigger(g1_node.trigger_id)
        g1_left_side_node_chance.new_effect.deactivate_trigger(g1_left_side_node_chance.trigger_id)
        g1_left_side_node_chance.new_effect.deactivate_trigger(g1_left_side_node_chance_negative.trigger_id)

        g1_left_side_node_chance_negative.new_effect.activate_trigger(g1_left_side_node.trigger_id)
        g1_left_side_node_chance_negative.new_effect.deactivate_trigger(g1_left_side_node_chance.trigger_id)
        g1_left_side_node_chance_negative.new_effect.deactivate_trigger(g1_left_side_node_chance_negative.trigger_id)
        if self.debug_messages:
            g1_left_side_node_chance_negative.new_effect.send_chat(message=f"G1 Left Side Node Chance Negative")

        # RIGHT RETURN
        g1_right_side_node.new_condition.timer(self.block1_period)
        g1_right_side_node.new_effect.activate_trigger(g1_right_side_node_chance.trigger_id)
        g1_right_side_node.new_effect.activate_trigger(g1_right_side_node_chance_negative.trigger_id)

        g1_right_side_node_chance.new_condition.chance(50)
        g1_right_side_node_chance.new_effect.activate_trigger(movement_list[0][1].trigger_id)
        g1_right_side_node_chance.new_effect.activate_trigger(movement_list[1][1].trigger_id)
        g1_right_side_node_chance.new_effect.activate_trigger(movement_list[4][1].trigger_id)
        g1_right_side_node_chance.new_effect.activate_trigger(movement_list[5][1].trigger_id)
        if self.debug_messages:
            g1_right_side_node_chance.new_effect.send_chat(message=f"G1 Right Side Node Chance")
        g1_right_side_node_chance.new_effect.activate_trigger(g1_node.trigger_id)
        g1_right_side_node_chance.new_effect.deactivate_trigger(g1_right_side_node_chance.trigger_id)
        g1_right_side_node_chance.new_effect.deactivate_trigger(g1_right_side_node_chance_negative.trigger_id)

        g1_right_side_node_chance_negative.new_effect.activate_trigger(g1_right_side_node.trigger_id)
        g1_right_side_node_chance_negative.new_effect.deactivate_trigger(g1_right_side_node_chance.trigger_id)
        g1_right_side_node_chance_negative.new_effect.deactivate_trigger(g1_right_side_node_chance_negative.trigger_id)
        if self.debug_messages:
            g1_right_side_node_chance_negative.new_effect.send_chat(message=f"G1 Right Side Node Chance Negative")

        # BLOCK 2
        block_2_list = [movement_list[i] for i in [9, 10, 11, 12]]
        self.two_node_graph("G Center", self.block2_period, block_2_list)
        for i in [6, 7, 8, 13, 14]:
            self.two_node_graph(f"G{i} Piece", self.block3_period, [movement_list[i]])

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
        for player in self.player_list:
            (UnitModifier(self.scenario, OtherInfo.MAP_REVEALER.ID, player)
             .modify_attribute(ObjectAttribute.LINE_OF_SIGHT, Operation.SET, 1)
             .create_triggers())
        (UnitModifier(self.scenario, BuildingInfo.WOODEN_BRIDGE_A_MIDDLE.ID, PlayerId.GAIA)
         .modify_attribute(ObjectAttribute.DEAD_UNIT_ID, Operation.SET, -1)
         .modify_attribute(ObjectAttribute.FOUNDATION_TERRAIN, Operation.SET, TerrainId.UNDERBRUSH_JUNGLE)
         .modify_attribute(ObjectAttribute.STANDING_GRAPHIC, Operation.SET, 0)
         .modify_attribute(ObjectAttribute.HIT_POINTS, Operation.SET, 0)
         .create_triggers())
        (UnitModifier(self.scenario, BuildingInfo.WOODEN_BRIDGE_B_MIDDLE.ID, PlayerId.GAIA)
         .modify_attribute(ObjectAttribute.DEAD_UNIT_ID, Operation.SET, -1)
         .modify_attribute(ObjectAttribute.FOUNDATION_TERRAIN, Operation.SET, TerrainId.FOREST_PINE)
         .modify_attribute(ObjectAttribute.STANDING_GRAPHIC, Operation.SET, 0)
         .modify_attribute(ObjectAttribute.HIT_POINTS, Operation.SET, 0)
         .create_triggers())
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
         .modify_attribute(ObjectAttribute.FOG_VISIBILITY, Operation.SET, 1)
         .modify_attribute(ObjectAttribute.STANDING_GRAPHIC, Operation.SET, 2310)
         .modify_attribute(ObjectAttribute.WALKING_GRAPHIC, Operation.SET, 2310)
         .modify_attribute(ObjectAttribute.ICON_ID, Operation.SET, OtherInfo.TREE_PINE_FOREST.ICON_ID)
         .modify_attribute(ObjectAttribute.OBJECT_NAME_ID, Operation.SET, 5399)
         .create_triggers())

    def move_trees(self, i: int, source_area: Area, target_area: Area, reverse: bool):
        source_tiles = source_area.to_coords()
        target_tiles = target_area.to_coords()
        title_string = "Way" if not reverse else "Return"
        trees_phase_1 = self.trigger_manager.add_trigger(f"Movement {i}:{title_string} | Phase 1", enabled=False)
        trees_phase_2 = self.trigger_manager.add_trigger(f"Movement {i}:{title_string} | Phase 2", enabled=False)
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
            trees_phase_1.new_effect.create_object(
                object_list_unit_id=BuildingInfo.WOODEN_BRIDGE_A_MIDDLE.ID,
                source_player=PlayerId.GAIA,
                location_x=source_tile.x,
                location_y=source_tile.y
            )
            for player in self.player_list:
                trees_phase_1.new_effect.create_object(
                    object_list_unit_id=OtherInfo.MAP_REVEALER.ID,
                    source_player=player,
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
        trees_phase_1.new_effect.activate_trigger(self.remove_revealer_trigger.trigger_id)

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
                object_list_unit_id=BuildingInfo.WOODEN_BRIDGE_B_MIDDLE.ID,
                source_player=PlayerId.GAIA,
                location_x=target_tile.x,
                location_y=target_tile.y
            )
            for player in self.player_list:
                trees_phase_2.new_effect.create_object(
                    object_list_unit_id=OtherInfo.MAP_REVEALER.ID,
                    source_player=player,
                    location_x=target_tile.x,
                    location_y=target_tile.y
                )
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
        trees_phase_2.new_effect.activate_trigger(self.remove_revealer_trigger.trigger_id)
        return trees_phase_1

    def two_node_graph(self, name: str, period: int, list_triggers: list[tuple[Trigger, Trigger]]):
        g2_node = self.trigger_manager.add_trigger(f'{name} Node', enabled=True, looping=False)
        g2_node_chance = self.trigger_manager.add_trigger(f'{name} Chance Node', enabled=False)
        g2_node_chance_negative = self.trigger_manager.add_trigger(f'{name} Chance Node Negative', enabled=False)

        g2_return_node = self.trigger_manager.add_trigger(f'{name} Return Node', enabled=False, looping=False)
        g2_return_node_chance = self.trigger_manager.add_trigger(f'{name} Return Node Chance', enabled=False)
        g2_return_node_chance_negative = self.trigger_manager.add_trigger(f'{name} Return Node Chance Negative', enabled=False)

        g2_node.new_condition.timer(period)
        g2_node.new_effect.activate_trigger(g2_node_chance.trigger_id)
        g2_node.new_effect.activate_trigger(g2_node_chance_negative.trigger_id)

        g2_node_chance.new_condition.chance(50)
        for trigger in list_triggers:
            g2_node_chance.new_effect.activate_trigger(trigger[0].trigger_id)
        if self.debug_messages:
            g2_node_chance.new_effect.send_chat(message=f"{name} Way Node Chance")
        g2_node_chance.new_effect.activate_trigger(g2_return_node.trigger_id)
        g2_node_chance.new_effect.deactivate_trigger(g2_node_chance.trigger_id)
        g2_node_chance.new_effect.deactivate_trigger(g2_node_chance_negative.trigger_id)

        g2_node_chance_negative.new_effect.activate_trigger(g2_node.trigger_id)
        g2_node_chance_negative.new_effect.deactivate_trigger(g2_node_chance.trigger_id)
        g2_node_chance_negative.new_effect.deactivate_trigger(g2_node_chance_negative.trigger_id)
        if self.debug_messages:
            g2_node_chance_negative.new_effect.send_chat(message=f"{name} Way Node Chance Negative")

        g2_return_node.new_condition.timer(period)
        g2_return_node.new_effect.activate_trigger(g2_return_node_chance.trigger_id)
        g2_return_node.new_effect.activate_trigger(g2_return_node_chance_negative.trigger_id)

        g2_return_node_chance.new_condition.chance(50)
        for trigger in list_triggers:
            g2_return_node_chance.new_effect.activate_trigger(trigger[1].trigger_id)
        if self.debug_messages:
            g2_return_node_chance.new_effect.send_chat(message=f"{name} Return Node Chance")
        g2_return_node_chance.new_effect.activate_trigger(g2_node.trigger_id)
        g2_return_node_chance.new_effect.deactivate_trigger(g2_return_node_chance.trigger_id)
        g2_return_node_chance.new_effect.deactivate_trigger(g2_return_node_chance_negative.trigger_id)

        g2_return_node_chance_negative.new_effect.activate_trigger(g2_return_node.trigger_id)
        g2_return_node_chance_negative.new_effect.deactivate_trigger(g2_return_node_chance.trigger_id)
        g2_return_node_chance_negative.new_effect.deactivate_trigger(g2_return_node_chance_negative.trigger_id)
        if self.debug_messages:
            g2_return_node_chance_negative.new_effect.send_chat(message=f"{name} Return Node Chance Negative")


if __name__ == '__main__':
    maze_runner = MazeRunner(
        input_scenario_name='EDIT_MAZE_RUNNER_1V1',
        output_scenario_name='OUTPUT_MAZE_RUNNER_1V1'
    )
    maze_runner.convert()

