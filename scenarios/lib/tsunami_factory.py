import itertools
import math

from AoE2ScenarioParser.datasets.players import PlayerId
from AoE2ScenarioParser.datasets.trigger_lists import ObjectAttribute, Operation, TerrainRestrictions, ActionType, AttackStance, PanelLocation
from AoE2ScenarioParser.datasets.units import UnitInfo
from AoE2ScenarioParser.objects.managers.trigger_manager import TriggerManager
from AoE2ScenarioParser.objects.support.tile import Tile
from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario

from scenarios.lib import transformations
from scenarios.lib.area_optimizer import AreaOptimizer
from scenarios.lib.random_probability import EqualRandomProbability
from scenarios.lib.unit_modifier import UnitModifier


class TsunamiFactory:
    MOVEMENT_DAMAGE = 152

    def __init__(self,
                 scenario: AoE2DEScenario,
                 tsunami_sound_name: str,
                 tsunami_speed: int,
                 tsunami_unit_damage: int,
                 player_list: list[PlayerId]):
        self.scenario = scenario
        self.map_manager = scenario.map_manager
        self.trigger_manager: TriggerManager = scenario.trigger_manager
        self.tsunami_sound_name = tsunami_sound_name
        self.tsunami_speed = tsunami_speed
        self.tsunami_unit_damage = tsunami_unit_damage
        self.player_list = player_list
        self.slopes = set()

    def tsunami_stats(self):
        (UnitModifier(self.scenario, UnitInfo.TIGER.ID, PlayerId.GAIA)
         .modify_attribute(ObjectAttribute.HIT_POINTS, Operation.SET, 20000)
         .modify_attribute(ObjectAttribute.UNIT_SIZE_X, Operation.SET, 0)
         .modify_attribute(ObjectAttribute.UNIT_SIZE_Y, Operation.SET, 0)
         .modify_attribute(ObjectAttribute.UNIT_SIZE_Z, Operation.SET, 0)
         .modify_attribute(ObjectAttribute.STANDING_GRAPHIC, Operation.SET, 7569)
         .modify_attribute(ObjectAttribute.WALKING_GRAPHIC, Operation.SET, 7569)
         .modify_attribute(ObjectAttribute.ATTACK_GRAPHIC, Operation.SET, 7569)
         .modify_attribute(ObjectAttribute.DYING_GRAPHIC, Operation.SET, 5507)
         .modify_attribute(ObjectAttribute.DEAD_UNIT_ID, Operation.SET, -2)
         .modify_attribute(ObjectAttribute.DEAD_UNIT_ID, Operation.DIVIDE, 2)
         .modify_attribute(ObjectAttribute.TERRAIN_RESTRICTION_ID, Operation.SET, TerrainRestrictions.ALL)
         .modify_attribute(ObjectAttribute.MOVEMENT_SPEED, Operation.SET, self.tsunami_speed)
         .create_triggers()
         )
        movement_damage_script = f'''void tsunami_movement_damage(){{             
                    xsTaskAmount(0, {self.tsunami_unit_damage});
                    xsTaskAmount(1, 1);
                    xsTaskAmount(2, 0.5);
                    xsTaskAmount(4, 0);
                    xsTaskAmount(5, 2);
                    xsTaskAmount(6, 5);
                    xsTask({UnitInfo.TIGER.ID}, {self.MOVEMENT_DAMAGE}, -1, {PlayerId.GAIA});
                }}
               '''
        movement_damage_trigger = self.trigger_manager.add_trigger("Movement Damage Script")
        movement_damage_trigger.new_effect.script_call(message=movement_damage_script)

    def config_tsunami(self, tile_list: list[Tile], amplitude: int, thickness: float, wave_delay: int, tsunami_periods: list[int], display_sound: bool = False):
        tsunami_init_wave = self.generate_tsunami_trigger(tile_list[0], tile_list[1], amplitude, thickness, wave_delay, display_sound=display_sound)
        period_triggers = [self.trigger_manager.add_trigger(f"Period Trigger {i}", enabled=False) for i, _ in enumerate(tsunami_periods)]
        for i, trigger in enumerate(period_triggers):
            trigger.new_condition.timer(tsunami_periods[i])
            trigger.new_effect.activate_trigger(tsunami_init_wave.trigger_id)
        random_period = EqualRandomProbability(self.trigger_manager, period_triggers, "Random Period")
        tsunami_init_wave.new_effect.activate_trigger(random_period.enable_probability_trigger.trigger_id)
        random_period.enable_probability_trigger.enabled = True

    def border_check(self, top_left: bool = False, top_right: bool = False, bottom_left: bool = False, bottom_right: bool = False):
        border_check = self.trigger_manager.add_trigger("Border Check", enabled=True, looping=True)
        if top_left:
            border_check.new_effect.kill_object(
                object_list_unit_id=UnitInfo.TIGER.ID,
                area_x1=0,
                area_y1=0,
                area_x2=self.map_manager.map_width - 1,
                area_y2=2,
                source_player=PlayerId.GAIA
            )
        if top_right:
            border_check.new_effect.kill_object(
                object_list_unit_id=UnitInfo.TIGER.ID,
                area_x1=self.map_manager.map_width - 3,
                area_y1=0,
                area_x2=self.map_manager.map_width - 1,
                area_y2=self.map_manager.map_height - 1,
                source_player=PlayerId.GAIA
            )
        if bottom_left:
            border_check.new_effect.kill_object(
                object_list_unit_id=UnitInfo.TIGER.ID,
                area_x1=0,
                area_y1=0,
                area_x2=2,
                area_y2=self.map_manager.map_height - 1,
                source_player=PlayerId.GAIA
            )
        if bottom_right:
            border_check.new_effect.kill_object(
                object_list_unit_id=UnitInfo.TIGER.ID,
                area_x1=0,
                area_y1=self.map_manager.map_height - 3,
                area_x2=self.map_manager.map_width - 1,
                area_y2=self.map_manager.map_height - 1,
                source_player=PlayerId.GAIA
            )

    def generate_tsunami_trigger(self, tile1: Tile, tile2: Tile, amplitude: int, thickness: float, wave_delay: int, display_sound: bool = False):
        vector = [tile2.x - tile1.x, tile2.y - tile1.y]
        distance = (math.sqrt(vector[0] ** 2 + vector[1] ** 2))
        normal = (vector[0] / distance, vector[1] / distance)
        perpendicular = (-normal[1], normal[0])
        rot_angle = math.atan2(tile2.y - tile1.y, tile2.x - tile1.x)
        wave_list = []
        for x in range(0, int(distance)):
            rads = 2 * math.pi / ((distance - 1.0) / 2.0) * (x % (distance / 2.0))
            y = (((-math.cos(rads) + 1) / 2) * amplitude) + 1
            wave_list.append(y)
        wave_rect = [(x, y) for x in range(0, int(distance)) for y in range(0, amplitude * 2) if wave_list[x] - thickness < y < wave_list[x] + thickness]
        wave_tiles = [transformations.get_tile(transformations.rotate_and_translate_tile(tile, rot_angle, (tile1.x, tile1.y))) for tile in wave_rect]
        create_tsunami = self.trigger_manager.add_trigger("Create Tsunami", enabled=False, looping=False)
        move_tsunami = self.trigger_manager.add_trigger("Move Tsunami", enabled=False, looping=False)
        stop_waves_on_elevation = self.trigger_manager.add_trigger("Stop Waves On Elevation", enabled=True, looping=True)
        stop_waves_areas = []
        for tile in wave_tiles:
            x, y = tile
            slope_found = False
            while 0 <= x < self.map_manager.map_width and 0 <= y < self.map_manager.map_height:
                direction_tile = self.map_manager.get_tile(int(x), int(y))
                if direction_tile.elevation == 1 and not slope_found:
                    for dx, dy in itertools.product((-1, 0, 1), repeat=2):
                        if (dx == 0 and dy == 0) or not (0 <= direction_tile.x + dx < self.map_manager.map_width) or not (0 <= direction_tile.y + dy < self.map_manager.map_height):
                            continue
                        new_tile = self.map_manager.get_tile(direction_tile.x + dx, direction_tile.y + dy)
                        if new_tile not in self.slopes and new_tile.elevation == 0:
                            self.slopes.add(new_tile)
                            slope_found = True
                            area = self.scenario.new.area()
                            area.x1 = int(new_tile.x)
                            area.y1 = int(new_tile.y)
                            area.x2 = int(new_tile.x + 1)
                            area.y2 = int(new_tile.y + 1)
                            stop_waves_areas.append(area)
                x += perpendicular[0]
                y += perpendicular[1]
            x = int(x - perpendicular[0])
            y = int(y - perpendicular[1])
            move_tsunami.new_effect.task_object(
                object_list_unit_id=UnitInfo.TIGER.ID,
                location_x=x,
                location_y=y,
                area_x1=tile.x,
                area_x2=tile.x,
                area_y1=tile.y,
                area_y2=tile.y,
                source_player=PlayerId.GAIA,
                action_type=ActionType.MOVE
            )
            create_tsunami.new_effect.create_object(
                source_player=PlayerId.GAIA,
                object_list_unit_id=UnitInfo.TIGER.ID,
                location_x=tile.x,
                location_y=tile.y
            )

        area_optimizer = AreaOptimizer(self.scenario)
        new_areas = area_optimizer.optimize_area(area_list=stop_waves_areas)
        print(f'Initial tsunami tiles: {len(stop_waves_areas)}, areas: {len(new_areas)}')
        for area in new_areas:
            stop_waves_on_elevation.new_effect.kill_object(
                object_list_unit_id=UnitInfo.TIGER.ID,
                source_player=PlayerId.GAIA,
                area_x1=area.x1,
                area_y1=area.y1,
                area_x2=area.x2,
                area_y2=area.y2
            )

        create_tsunami.new_effect.change_object_stance(
            source_player=PlayerId.GAIA,
            object_list_unit_id=UnitInfo.TIGER.ID,
            attack_stance=AttackStance.NO_ATTACK_STANCE
        )
        create_tsunami.new_effect.disable_unit_targeting(
            source_player=PlayerId.GAIA,
            object_list_unit_id=UnitInfo.TIGER.ID
        )
        create_tsunami.new_effect.disable_object_selection(
            source_player=PlayerId.GAIA,
            object_list_unit_id=UnitInfo.TIGER.ID
        )
        create_tsunami.new_effect.activate_trigger(
            trigger_id=move_tsunami.trigger_id
        )
        first_wave = self.trigger_manager.add_trigger("First Wave", enabled=False)
        second_wave = self.trigger_manager.add_trigger("Second Wave", enabled=False)
        third_wave = self.trigger_manager.add_trigger("Third Wave", enabled=False)
        first_wave.new_effect.activate_trigger(create_tsunami.trigger_id)
        first_wave.new_effect.activate_trigger(second_wave.trigger_id)
        first_wave.new_effect.activate_trigger(third_wave.trigger_id)
        if display_sound:
            first_wave.new_effect.display_instructions(
                object_list_unit_id=UnitInfo.GALLEON.ID,
                source_player=PlayerId.GAIA,
                sound_name=self.tsunami_sound_name,
                message="The Tsunami is coming!",
                display_time=30,
                instruction_panel_position=PanelLocation.MIDDLE
            )
        second_wave.new_condition.timer(wave_delay)
        second_wave.new_effect.activate_trigger(create_tsunami.trigger_id)
        third_wave.new_condition.timer(wave_delay * 2)
        third_wave.new_effect.activate_trigger(create_tsunami.trigger_id)
        return first_wave
