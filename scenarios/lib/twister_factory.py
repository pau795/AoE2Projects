import math

from AoE2ScenarioParser.datasets.players import PlayerId
from AoE2ScenarioParser.datasets.trigger_lists import ActionType, AttackStance, ObjectAttribute, Operation, FogVisibility
from AoE2ScenarioParser.datasets.units import UnitInfo
from AoE2ScenarioParser.objects.managers.trigger_manager import TriggerManager
from AoE2ScenarioParser.objects.support.tile import Tile
from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario

from scenarios.lib.random_probability import EqualRandomProbability
from scenarios.lib.unit_modifier import UnitModifier


class TwisterFactory:

    def __init__(self,
                 scenario: AoE2DEScenario,
                 twister_sound_name: str,
                 sound_delay: int,
                 player_list: list[PlayerId]):
        self.scenario = scenario
        self.trigger_manager: TriggerManager = scenario.trigger_manager
        self.sound_delay = sound_delay
        self.twister_sound_name = twister_sound_name
        self.player_list = player_list

    def twister_stats(self):
        (UnitModifier(self.scenario, UnitInfo.SNOW_LEOPARD.ID, PlayerId.GAIA)
         .modify_attribute(ObjectAttribute.HIT_POINTS, Operation.SET, 20000)
         .modify_attribute(ObjectAttribute.UNIT_SIZE_X, Operation.DIVIDE, 10)
         .modify_attribute(ObjectAttribute.UNIT_SIZE_Y, Operation.DIVIDE, 10)
         .modify_attribute(ObjectAttribute.UNIT_SIZE_Z, Operation.SET, 0)
         .modify_attribute(ObjectAttribute.STANDING_GRAPHIC, Operation.SET, 5314)
         .modify_attribute(ObjectAttribute.WALKING_GRAPHIC, Operation.SET, 5314)
         .modify_attribute(ObjectAttribute.ATTACK_GRAPHIC, Operation.SET, 5314)
         .modify_attribute(ObjectAttribute.MOVEMENT_SPEED, Operation.SET, 5)
         .modify_attribute(ObjectAttribute.TERRAIN_RESTRICTION_ID, Operation.SET, 0)
         .modify_attribute(ObjectAttribute.FOG_VISIBILITY, Operation.SET, FogVisibility.ALWAYS_VISIBLE)
         .modify_attribute(ObjectAttribute.ATTACK, Operation.SET, 0, 4)
         .create_triggers()
         )

    def twister_sound(self):
        tornado_sound = self.trigger_manager.add_trigger("Tornado Sound", enabled=False)
        tornado_sound_delay = self.trigger_manager.add_trigger("Tornado Sound Delay", enabled=True)

        tornado_sound_delay.new_condition.timer(timer=self.sound_delay)
        tornado_sound_delay.new_effect.activate_trigger(trigger_id=tornado_sound.trigger_id)

        for player in self.player_list:
            tornado_sound.new_effect.play_sound(
                source_player=player,
                sound_name=self.twister_sound_name
            )
        tornado_sound.new_effect.activate_trigger(trigger_id=tornado_sound_delay.trigger_id)

    def spawn_tornado(self,
                      center: Tile,
                      radius: int,
                      arms: int,
                      drag_radius: int,
                      inner_radius: int,
                      spawn_times: list[int],
                      duration_times: list[int],
                      ):
        outer_radius = drag_radius - inner_radius
        create_units_tornado = self.trigger_manager.add_trigger("Create Units Tornado", enabled=False)
        task_units_tornado = self.trigger_manager.add_trigger("Task Units Tornado", looping=True, enabled=False)

        for i in range(inner_radius, radius, 1):
            for j in range(0, arms):
                angle1 = j * 2 * math.pi / arms
                angle2 = ((j - 1) % arms) * 2 * math.pi / arms
                init_x1 = round(center.x + i * math.cos(angle1))
                init_y1 = round(center.y + i * math.sin(angle1))
                init_x2 = round(center.x + i * math.cos(angle2))
                init_y2 = round(center.y + i * math.sin(angle2))
                init_x1, init_x2 = (init_x1, init_x2) if init_x1 < init_x2 else (init_x2, init_x1)
                init_y1, init_y2 = (init_y1, init_y2) if init_y1 < init_y2 else (init_y2, init_y1)
                end_x = round(center.x + i * math.cos(((j + 1) % arms) * 2 * math.pi / arms))
                end_y = round(center.y + i * math.sin(((j + 1) % arms) * 2 * math.pi / arms))
                create_units_tornado.new_effect.create_object(
                    source_player=PlayerId.GAIA,
                    location_x=init_x1,
                    location_y=init_y1,
                    object_list_unit_id=UnitInfo.SNOW_LEOPARD.ID
                )
                task_units_tornado.new_effect.task_object(
                    source_player=PlayerId.GAIA,
                    area_x1=init_x1,
                    area_y1=init_y1,
                    area_x2=init_x2,
                    area_y2=init_y2,
                    location_x=end_x,
                    location_y=end_y,
                    object_list_unit_id=UnitInfo.SNOW_LEOPARD.ID,
                    action_type=ActionType.MOVE

                )
        create_units_tornado.new_effect.change_object_stance(
            source_player=PlayerId.GAIA,
            object_list_unit_id=UnitInfo.SNOW_LEOPARD.ID,
            attack_stance=AttackStance.NO_ATTACK_STANCE
        )

        area_left = self.scenario.new.area()
        area_left.x1 = center.x - drag_radius
        area_left.y1 = center.y - drag_radius
        area_left.x2 = center.x - drag_radius + outer_radius
        area_left.y2 = center.y + drag_radius

        area_bottom = self.scenario.new.area()
        area_bottom.x1 = center.x - drag_radius
        area_bottom.y1 = center.y + drag_radius - outer_radius
        area_bottom.x2 = center.x + drag_radius
        area_bottom.y2 = center.y + drag_radius

        area_right = self.scenario.new.area()
        area_right.x1 = center.x + drag_radius - outer_radius
        area_right.y1 = center.y - drag_radius
        area_right.x2 = center.x + drag_radius
        area_right.y2 = center.y + drag_radius

        area_top = self.scenario.new.area()
        area_top.x1 = center.x - drag_radius
        area_top.y1 = center.y - drag_radius
        area_top.x2 = center.x + drag_radius
        area_top.y2 = center.y - drag_radius + outer_radius

        center_area = self.scenario.new.area()
        center_area.x1 = center.x - inner_radius + 1
        center_area.y1 = center.y - inner_radius + 1
        center_area.x2 = center.x + inner_radius - 1
        center_area.y2 = center.y + inner_radius - 1

        tornado_drag_triggers = []
        for player in self.player_list:
            tornado_drag = self.trigger_manager.add_trigger(f"Tornado Drag P{player.value}", looping=True, enabled=False)
            tornado_drag.new_effect.stop_object(
                source_player=player,
                area_x1=area_left.x1,
                area_y1=area_left.y1,
                area_x2=area_left.x2,
                area_y2=area_left.y2,
            )

            tornado_drag.new_effect.stop_object(
                source_player=player,
                area_x1=area_bottom.x1,
                area_y1=area_bottom.y1,
                area_x2=area_bottom.x2,
                area_y2=area_bottom.y2,
            )

            tornado_drag.new_effect.stop_object(
                source_player=player,
                area_x1=area_right.x1,
                area_y1=area_right.y1,
                area_x2=area_right.x2,
                area_y2=area_right.y2,
            )

            tornado_drag.new_effect.stop_object(
                source_player=player,
                area_x1=area_top.x1,
                area_y1=area_top.y1,
                area_x2=area_top.x2,
                area_y2=area_top.y2,
            )

            tornado_drag.new_effect.task_object(
                source_player=player,
                area_x1=area_left.x1,
                area_y1=area_left.y1,
                area_x2=area_left.x2,
                area_y2=area_left.y2,
                location_x=center.x,
                location_y=center.y,
                action_type=ActionType.MOVE
            )

            tornado_drag.new_effect.task_object(
                source_player=player,
                area_x1=area_bottom.x1,
                area_y1=area_bottom.y1,
                area_x2=area_bottom.x2,
                area_y2=area_bottom.y2,
                location_x=center.x,
                location_y=center.y,
                action_type=ActionType.MOVE
            )

            tornado_drag.new_effect.task_object(
                source_player=player,
                area_x1=area_right.x1,
                area_y1=area_right.y1,
                area_x2=area_right.x2,
                area_y2=area_right.y2,
                location_x=center.x,
                location_y=center.y,
                action_type=ActionType.MOVE
            )

            tornado_drag.new_effect.task_object(
                source_player=player,
                area_x1=area_top.x1,
                area_y1=area_top.y1,
                area_x2=area_top.x2,
                area_y2=area_top.y2,
                location_x=center.x,
                location_y=center.y,
                action_type=ActionType.MOVE
            )

            tornado_drag.new_effect.disable_object_selection(
                source_player=player,
                area_x1=area_left.x1,
                area_y1=area_left.y1,
                area_x2=area_left.x2,
                area_y2=area_left.y2,
            )

            tornado_drag.new_effect.disable_object_selection(
                source_player=player,
                area_x1=area_bottom.x1,
                area_y1=area_bottom.y1,
                area_x2=area_bottom.x2,
                area_y2=area_bottom.y2,
            )

            tornado_drag.new_effect.disable_object_selection(
                source_player=player,
                area_x1=area_right.x1,
                area_y1=area_right.y1,
                area_x2=area_right.x2,
                area_y2=area_right.y2,
            )

            tornado_drag.new_effect.disable_object_selection(
                source_player=player,
                area_x1=area_top.x1,
                area_y1=area_top.y1,
                area_x2=area_top.x2,
                area_y2=area_top.y2,
            )

            tornado_drag.new_effect.enable_object_selection(
                source_player=player,
                area_x1=center_area.x1,
                area_y1=center_area.y1,
                area_x2=center_area.x2,
                area_y2=center_area.y2,
            )
            tornado_drag_triggers.append(tornado_drag)

        tornado_activate_triggers = [self.trigger_manager.add_trigger(f'Activate Tornado {i}', enabled=False)
                                     for i, x in enumerate(spawn_times)]
        tornado_duration_triggers = [self.trigger_manager.add_trigger(f'Tornado Duration {i}', enabled=False)
                                     for i, x in enumerate(duration_times)]

        activate_tornado_probability = EqualRandomProbability(
            self.trigger_manager, tornado_activate_triggers, "Activate Tornado"
        )
        activate_tornado_probability.enable_probability_trigger.enabled = True
        tornado_duration_probability = EqualRandomProbability(
            self.trigger_manager, tornado_duration_triggers, "Tornado Duration"
        )

        for i, trigger in enumerate(tornado_activate_triggers):
            trigger.new_condition.timer(spawn_times[i])
            trigger.new_effect.activate_trigger(trigger_id=create_units_tornado.trigger_id)
            trigger.new_effect.activate_trigger(trigger_id=task_units_tornado.trigger_id)
            for tornado_trigger in tornado_drag_triggers:
                trigger.new_effect.activate_trigger(trigger_id=tornado_trigger.trigger_id)
            trigger.new_effect.activate_trigger(
                trigger_id=tornado_duration_probability.enable_probability_trigger.trigger_id
            )

        for i, trigger in enumerate(tornado_duration_triggers):
            trigger.new_condition.timer(duration_times[i])
            trigger.new_effect.deactivate_trigger(trigger_id=create_units_tornado.trigger_id)
            trigger.new_effect.deactivate_trigger(trigger_id=task_units_tornado.trigger_id)
            for tornado_trigger in tornado_drag_triggers:
                trigger.new_effect.deactivate_trigger(trigger_id=tornado_trigger.trigger_id)
            trigger.new_effect.remove_object(
                object_list_unit_id=UnitInfo.SNOW_LEOPARD.ID,
                source_player=PlayerId.GAIA,
                area_x1=center.x - radius,
                area_y1=center.y - radius,
                area_x2=center.x + radius,
                area_y2=center.y + radius,
            )
            trigger.new_effect.enable_object_selection(
                source_player=PlayerId.ONE,
                area_x1=center.x - radius,
                area_y1=center.y - radius,
                area_x2=center.x + radius,
                area_y2=center.y + radius,
            )
            trigger.new_effect.enable_object_selection(
                source_player=PlayerId.TWO,
                area_x1=center.x - radius,
                area_y1=center.y - radius,
                area_x2=center.x + radius,
                area_y2=center.y + radius,
            )
            trigger.new_effect.activate_trigger(
                trigger_id=activate_tornado_probability.enable_probability_trigger.trigger_id
            )
