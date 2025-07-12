from AoE2ScenarioParser.datasets.players import PlayerId
from AoE2ScenarioParser.datasets.trigger_lists import ObjectClass, ActionType
from AoE2ScenarioParser.objects.managers.trigger_manager import TriggerManager
from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario
from AoE2ScenarioParser.scenarios.support.data_triggers import DataTriggers

players = [PlayerId.ONE, PlayerId.TWO, PlayerId.THREE, PlayerId.FOUR, PlayerId.FIVE, PlayerId.SIX, PlayerId.SEVEN, PlayerId.EIGHT]
area_names = {
    "arena_to_respawn": 0,
    "shop_to_respawn": 1,
    "respawn_to_arena": 2,
    "drop_to_respawn": 3,
    "drop_to_arena": 4,
    "respawn_task": 5,
    "arena_task": 6,
    "stone_return": 7,
    "stone_task": 8
}


class Teleports:

    def __init__(self, scenario: AoE2DEScenario, trigger_data: DataTriggers):
        self.trigger_manager: TriggerManager = scenario.trigger_manager
        self.trigger_data = trigger_data
        self.areas_teleport_source = self.trigger_data.areas['teleport_source']
        self.tiles_teleport_respawn = self.trigger_data.tiles['teleport_respawn']
        self.tiles_teleport_arena = self.trigger_data.tiles['teleport_arena']
        self.tiles_teleport_stone_return = self.trigger_data.tiles['teleport_stone_return']
        self.tiles_task_respawn = self.trigger_data.tiles['teleport_task_respawn']
        self.tiles_task_arena = self.trigger_data.tiles['teleport_task_arena']
        self.tiles_task_stone = self.trigger_data.tiles['teleport_task_stone']
        self.teleport_respawn()
        self.teleport_arena()
        self.teleport_stone()

    def teleport_respawn(self):
        for player in players:
            camara_to_respawn = self.trigger_manager.add_trigger(f'Change View to Respawn (p{player})', looping=True)
            teleport_to_respawn = self.trigger_manager.add_trigger(f'Teleport to Respawn (p{player})', looping=True)
            for x in [area_names["arena_to_respawn"], area_names["shop_to_respawn"], area_names["drop_to_respawn"]]:
                teleport_to_respawn.new_effect.stop_object(
                    source_player=player,
                    area_x1=self.areas_teleport_source[x].x1,
                    area_y1=self.areas_teleport_source[x].y1,
                    area_x2=self.areas_teleport_source[x].x2,
                    area_y2=self.areas_teleport_source[x].y2,
                    object_group=ObjectClass.CIVILIAN
                )
                teleport_to_respawn.new_effect.teleport_object(
                    source_player=player,
                    area_x1=self.areas_teleport_source[x].x1,
                    area_y1=self.areas_teleport_source[x].y1,
                    area_x2=self.areas_teleport_source[x].x2,
                    area_y2=self.areas_teleport_source[x].y2,
                    location_x=self.tiles_teleport_respawn[player.value - 1].x,
                    location_y=self.tiles_teleport_respawn[player.value - 1].y,
                    object_group=ObjectClass.CIVILIAN
                )
                camara_to_respawn.new_condition.objects_in_area(
                    source_player=player,
                    area_x1=self.areas_teleport_source[x].x1,
                    area_y1=self.areas_teleport_source[x].y1,
                    area_x2=self.areas_teleport_source[x].x2,
                    area_y2=self.areas_teleport_source[x].y2,
                    object_group=ObjectClass.CIVILIAN,
                    quantity=1
                )
                camara_to_respawn.new_condition.or_()
            camara_to_respawn.remove_condition(len(camara_to_respawn.conditions) - 1)
            teleport_to_respawn.new_effect.task_object(
                source_player=player,
                area_x1=self.areas_teleport_source[area_names["respawn_task"]].x1,
                area_y1=self.areas_teleport_source[area_names["respawn_task"]].y1,
                area_x2=self.areas_teleport_source[area_names["respawn_task"]].x2,
                area_y2=self.areas_teleport_source[area_names["respawn_task"]].y2,
                location_x=self.tiles_task_respawn[player.value - 1].x,
                location_y=self.tiles_task_respawn[player.value - 1].y,
                object_group=ObjectClass.CIVILIAN,
                action_type=ActionType.MOVE
            )
            camara_to_respawn.new_effect.change_view(
                source_player=player,
                location_x=self.tiles_teleport_respawn[player.value - 1].x,
                location_y=self.tiles_teleport_respawn[player.value - 1].y,
                scroll=True
            )

    def teleport_arena(self):
        for player in players:
            camara_to_arena = self.trigger_manager.add_trigger(f'Change view to Arena (p{player})', looping=True)
            teleport_to_arena = self.trigger_manager.add_trigger(f'Teleport to Arena (p{player})', looping=True)
            for x in [area_names["respawn_to_arena"], area_names["drop_to_arena"]]:
                teleport_to_arena.new_effect.stop_object(
                    source_player=player,
                    area_x1=self.areas_teleport_source[x].x1,
                    area_y1=self.areas_teleport_source[x].y1,
                    area_x2=self.areas_teleport_source[x].x2,
                    area_y2=self.areas_teleport_source[x].y2,
                    object_group=ObjectClass.CIVILIAN
                )
                teleport_to_arena.new_effect.teleport_object(
                    source_player=player,
                    area_x1=self.areas_teleport_source[x].x1,
                    area_y1=self.areas_teleport_source[x].y1,
                    area_x2=self.areas_teleport_source[x].x2,
                    area_y2=self.areas_teleport_source[x].y2,
                    location_x=self.tiles_teleport_arena[player.value - 1].x,
                    location_y=self.tiles_teleport_arena[player.value - 1].y,
                    object_group=ObjectClass.CIVILIAN
                )
                camara_to_arena.new_condition.objects_in_area(
                    source_player=player,
                    area_x1=self.areas_teleport_source[x].x1,
                    area_y1=self.areas_teleport_source[x].y1,
                    area_x2=self.areas_teleport_source[x].x2,
                    area_y2=self.areas_teleport_source[x].y2,
                    object_group=ObjectClass.CIVILIAN,
                    quantity=1
                )
                camara_to_arena.new_condition.or_()
            camara_to_arena.remove_condition(len(camara_to_arena.conditions) - 1)
            teleport_to_arena.new_effect.task_object(
                source_player=player,
                area_x1=self.areas_teleport_source[area_names["arena_task"]].x1,
                area_y1=self.areas_teleport_source[area_names["arena_task"]].y1,
                area_x2=self.areas_teleport_source[area_names["arena_task"]].x2,
                area_y2=self.areas_teleport_source[area_names["arena_task"]].y2,
                location_x=self.tiles_task_arena[player.value - 1].x,
                location_y=self.tiles_task_arena[player.value - 1].y,
                object_group=ObjectClass.CIVILIAN,
                action_type=ActionType.MOVE
            )
            camara_to_arena.new_effect.change_view(
                source_player=player,
                location_x=self.tiles_teleport_arena[player.value - 1].x,
                location_y=self.tiles_teleport_arena[player.value - 1].y,
                scroll=True,
            )

    def teleport_stone(self):
        for player in players:
            camara_to_stone_return = self.trigger_manager.add_trigger(f'Change view to Stone Return (p{player})', looping=True)
            teleport_to_stone_return = self.trigger_manager.add_trigger(f'Teleport to Stone Return (p{player})', looping=True)
            for x in [area_names["stone_return"]]:
                teleport_to_stone_return.new_effect.stop_object(
                    source_player=player,
                    area_x1=self.areas_teleport_source[x].x1,
                    area_y1=self.areas_teleport_source[x].y1,
                    area_x2=self.areas_teleport_source[x].x2,
                    area_y2=self.areas_teleport_source[x].y2,
                    object_group=ObjectClass.CIVILIAN
                )
                teleport_to_stone_return.new_effect.teleport_object(
                    source_player=player,
                    area_x1=self.areas_teleport_source[x].x1,
                    area_y1=self.areas_teleport_source[x].y1,
                    area_x2=self.areas_teleport_source[x].x2,
                    area_y2=self.areas_teleport_source[x].y2,
                    location_x=self.tiles_teleport_stone_return[player.value - 1].x,
                    location_y=self.tiles_teleport_stone_return[player.value - 1].y,
                    object_group=ObjectClass.CIVILIAN
                )
                camara_to_stone_return.new_condition.objects_in_area(
                    source_player=player,
                    area_x1=self.areas_teleport_source[x].x1,
                    area_y1=self.areas_teleport_source[x].y1,
                    area_x2=self.areas_teleport_source[x].x2,
                    area_y2=self.areas_teleport_source[x].y2,
                    object_group=ObjectClass.CIVILIAN,
                    quantity=1
                )
                camara_to_stone_return.new_condition.or_()
            camara_to_stone_return.remove_condition(len(camara_to_stone_return.conditions) - 1)
            teleport_to_stone_return.new_effect.task_object(
                source_player=player,
                area_x1=self.areas_teleport_source[area_names["stone_task"]].x1,
                area_y1=self.areas_teleport_source[area_names["stone_task"]].y1,
                area_x2=self.areas_teleport_source[area_names["stone_task"]].x2,
                area_y2=self.areas_teleport_source[area_names["stone_task"]].y2,
                location_x=self.tiles_task_stone[player.value - 1].x,
                location_y=self.tiles_task_stone[player.value - 1].y,
                object_group=ObjectClass.CIVILIAN,
                action_type=ActionType.MOVE
            )
            camara_to_stone_return.new_effect.change_view(
                source_player=player,
                location_x=self.tiles_teleport_stone_return[player.value - 1].x,
                location_y=self.tiles_teleport_stone_return[player.value - 1].y,
                scroll=True,
            )
