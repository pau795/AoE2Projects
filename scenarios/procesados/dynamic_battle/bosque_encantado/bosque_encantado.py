import math

from AoE2ScenarioParser.datasets.other import OtherInfo
from AoE2ScenarioParser.datasets.players import PlayerId
from AoE2ScenarioParser.datasets.trigger_lists import Operation, ObjectAttribute, AttackStance, TerrainRestrictions, ObjectState
from AoE2ScenarioParser.datasets.units import UnitInfo

from scenarios.lib.parser_project import ParserProject
from scenarios.lib.civ_settings import CivSettings
from scenarios.lib.unit_modifier import UnitModifier


class BosqueEncantado(ParserProject):

    def __init__(self, input_scenario_name: str, output_scenario_name: str):
        super().__init__(input_scenario_name, output_scenario_name)
        self.player_list = [PlayerId.ONE, PlayerId.TWO]
        self.trigger_manager = self.scenario.trigger_manager
        self.data_triggers = self.scenario.actions.load_data_triggers()
        self.leopard_speed = 2
        self.forest_delay = 300
        self.sound = 'tree_roots'
        self.tree_respawn_end = 40 * 60

    @staticmethod
    def calculate_delay(i):
        if 0 < i <= 4:
            return 300
        elif 4 < i <= 8:
            return 600
        elif 13 < i <= 24:
            return 900
        elif 8 < i <= 12:
            return 1200
        else:
            return 1

    def process(self):
        CivSettings(self.scenario, self.player_list)
        self.stats()
        self.sounds()
        self.end_tree_respawn()
        for i, (key, areas) in enumerate(self.data_triggers.areas.items()):
            initial_forest_delay = self.trigger_manager.add_trigger(f'{key} initial forest delay', enabled=True)
            initial_forest_delay.new_condition.timer(self.calculate_delay(i + 1))
            ti1, _, _ = self.move_trees(f'{key} init', (areas[0], areas[1]))
            initial_forest_delay.new_effect.activate_trigger(trigger_id=ti1.trigger_id)

    def sounds(self):
        for time in [300, 600, 900, 1200]:
            trigger = self.trigger_manager.add_trigger(f'Forest Sound {time}')
            trigger.new_condition.timer(self.forest_delay + time)
            for player in self.player_list:
                trigger.new_effect.play_sound(
                    sound_name='tree_roots',
                    source_player=player
                )

    def end_tree_respawn(self):
        end_tree_respawn = self.trigger_manager.add_trigger('End Tree Respawn')
        end_tree_respawn.new_condition.timer(self.tree_respawn_end)
        end_tree_respawn.new_effect.modify_attribute(
            object_list_unit_id=OtherInfo.TREE_PINE_FOREST.ID,
            source_player=PlayerId.GAIA,
            object_attributes=ObjectAttribute.DEAD_UNIT_ID,
            operation=Operation.SET,
            quantity=OtherInfo.TREE_PINE_FOREST.DEAD_ID
        )

    def stats(self):
        (UnitModifier(self.scenario, OtherInfo.TREE_PINE_FOREST.ID, PlayerId.GAIA)
         .modify_attribute(ObjectAttribute.DEAD_UNIT_ID, Operation.SET, OtherInfo.TREE_PINE_FOREST.ID)
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

    def move_trees(self, key, area_pair):
        source_tiles = area_pair[0].to_coords()
        target_tiles = area_pair[1].to_coords()
        distance = math.dist(area_pair[0].get_center(), area_pair[1].get_center())
        transform_trees_to_leopards = self.trigger_manager.add_trigger(f"{key} - Trees -> Leopards", enabled=False)
        move_leopards = self.trigger_manager.add_trigger(f"{key} - Move Leopards", enabled=False)
        transform_leopards_to_trees = self.trigger_manager.add_trigger(f"{key} - Leopards -> Trees", enabled=False)
        transform_trees_to_leopards.new_condition.timer(self.forest_delay)

        transform_trees_to_leopards.new_effect.remove_object(
            object_list_unit_id=OtherInfo.TREE_PINE_FOREST.ID,
            source_player=PlayerId.GAIA,
            object_state=ObjectState.RESOURCE,
            area_x1=area_pair[0].x1,
            area_y1=area_pair[0].y1,
            area_x2=area_pair[0].x2,
            area_y2=area_pair[0].y2
        )
        transform_trees_to_leopards.new_effect.replace_object(
            object_list_unit_id=OtherInfo.TREE_PINE_FOREST.ID,
            source_player=PlayerId.GAIA,
            object_list_unit_id_2=UnitInfo.SNOW_LEOPARD.ID,
            target_player=PlayerId.GAIA,
            area_x1=area_pair[0].x1,
            area_y1=area_pair[0].y1,
            area_x2=area_pair[0].x2,
            area_y2=area_pair[0].y2
        )
        transform_trees_to_leopards.new_effect.change_object_stance(
            object_list_unit_id=UnitInfo.SNOW_LEOPARD.ID,
            source_player=PlayerId.GAIA,
            area_x1=area_pair[0].x1,
            area_y1=area_pair[0].y1,
            area_x2=area_pair[0].x2,
            area_y2=area_pair[0].y2,
            attack_stance=AttackStance.NO_ATTACK_STANCE
        )

        transform_trees_to_leopards.new_effect.disable_object_selection(
            object_list_unit_id=UnitInfo.SNOW_LEOPARD.ID,
            source_player=PlayerId.GAIA,
            area_x1=area_pair[0].x1,
            area_y1=area_pair[0].y1,
            area_x2=area_pair[0].x2,
            area_y2=area_pair[0].y2
        )
        transform_trees_to_leopards.new_effect.disable_unit_targeting(
            object_list_unit_id=UnitInfo.SNOW_LEOPARD.ID,
            source_player=PlayerId.GAIA,
            area_x1=area_pair[0].x1,
            area_y1=area_pair[0].y1,
            area_x2=area_pair[0].x2,
            area_y2=area_pair[0].y2
        )
        transform_trees_to_leopards.new_effect.activate_trigger(
            trigger_id=move_leopards.trigger_id
        )
        transform_trees_to_leopards.new_effect.activate_trigger(
            trigger_id=transform_leopards_to_trees.trigger_id
        )

        for i, tile in enumerate(source_tiles):
            move_leopards.new_effect.task_object(
                object_list_unit_id=UnitInfo.SNOW_LEOPARD.ID,
                source_player=PlayerId.GAIA,
                area_x1=tile.x,
                area_y1=tile.y,
                area_x2=tile.x,
                area_y2=tile.y,
                location_x=target_tiles[i].x,
                location_y=target_tiles[i].y
            )
        rotation = area_pair[0].get_width() != area_pair[1].get_width()
        timer = int(math.ceil(distance / self.leopard_speed) + (4 * (2 if rotation else 1))) + 1
        transform_leopards_to_trees.new_condition.timer(timer)
        for player in self.player_list:
            transform_leopards_to_trees.new_effect.kill_object(
                source_player=player,
                area_x1=max(0, area_pair[1].x1 - 1),
                area_y1=max(0, area_pair[1].y1 - 1),
                area_x2=min(self.scenario.map_manager.map_width - 1, area_pair[1].x2 + 1),
                area_y2=min(self.scenario.map_manager.map_height - 1, area_pair[1].y2 + 1),
            )
        transform_leopards_to_trees.new_effect.replace_object(

            object_list_unit_id=UnitInfo.SNOW_LEOPARD.ID,
            source_player=PlayerId.GAIA,
            object_list_unit_id_2=OtherInfo.TREE_PINE_FOREST.ID,
            target_player=PlayerId.GAIA,
            area_x1=max(0, area_pair[1].x1 - 1),
            area_y1=max(0, area_pair[1].y1 - 1),
            area_x2=min(self.scenario.map_manager.map_width - 1, area_pair[1].x2 + 1),
            area_y2=min(self.scenario.map_manager.map_height - 1, area_pair[1].y2 + 1),
        )
        return transform_trees_to_leopards, move_leopards, transform_leopards_to_trees

if __name__ == '__main__':
    bosque_encantado = BosqueEncantado(
        input_scenario_name='BOSQUE ENCANTADO',
        output_scenario_name='BOSQUE ENCANTADO_output'
    )
    bosque_encantado.convert()
