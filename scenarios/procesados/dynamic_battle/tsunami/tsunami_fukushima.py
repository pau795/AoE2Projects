import itertools
import math

from AoE2ScenarioParser.datasets.players import PlayerId
from AoE2ScenarioParser.datasets.projectiles import ProjectileInfo
from AoE2ScenarioParser.datasets.trigger_lists import ObjectAttribute, Operation, CombatAbility, TerrainRestrictions, ActionType, AttackStance, ProjectileHitMode, DamageClass, \
    Comparison
from AoE2ScenarioParser.datasets.units import UnitInfo
from AoE2ScenarioParser.objects.support.tile import Tile

from scenarios.lib import transformations
from scenarios.lib.parser_project import ParserProject
from scenarios.lib.random_probability import EqualRandomProbability
from scenarios.lib.civ_settings import CivSettings
from scenarios.lib.unit_modifier import UnitModifier


class Tsunami2(ParserProject):

    def __init__(self, input_scenario_name: str, output_scenario_name: str):
        super().__init__(input_scenario_name, output_scenario_name)
        self.map_manager = self.scenario.map_manager
        self.trigger_manager = self.scenario.trigger_manager
        self.unit_manager = self.scenario.unit_manager
        self.tsunami_initial_delay = 600
        self.tsunami_periods = [450, 480, 510, 540, 570, 600]
        self.tsunami_wave_delay = 15
        self.tsunami_speed = 2
        self.tsunami_unit_damage = 7
        self.tsunami_building_damage = 10
        self.tsunami_sound = 'sirena60'
        self.player_list = [PlayerId.ONE, PlayerId.TWO]
        self.data_triggers = self.scenario.actions.load_data_triggers()
        self.left_tsunami = self.data_triggers.tiles["left_tsunami"]
        self.right_tsunami = self.data_triggers.tiles["right_tsunami"]
        self.diagonal_tsunami = self.data_triggers.tiles["diagonal_tsunami"]
        self.quit_units = self.trigger_manager.add_trigger("Quit Units", enabled=False, looping=False)
        self.quit_units.new_condition.timer(timer=10)
        self.quit_units.new_effect.remove_object(
            source_player=PlayerId.THREE,
            object_list_unit_id=UnitInfo.CHAKRAM_THROWER.ID
        )

    def process(self):
        CivSettings(self.scenario, self.player_list)
        self.p3_stats()
        self.stop_waves_on_elevation()
        self.create_tsunamis()

    def p3_stats(self):
        tsunami_variable = self.trigger_manager.add_trigger("Tsunami Variable")
        tsunami_variable.new_effect.change_variable(
            variable=0,
            quantity=0,
            message="Tsunami Variable"
        )
        p3_target = self.trigger_manager.add_trigger("P3 Target")
        p3_target.new_effect.disable_unit_targeting(
            source_player=PlayerId.THREE,
            object_list_unit_id=UnitInfo.HORSE_A.ID
        )
        p3_target.new_effect.disable_object_selection(
            source_player=PlayerId.THREE,
            object_list_unit_id=UnitInfo.HORSE_A.ID
        )
        (UnitModifier(self.scenario, UnitInfo.VULTURE.ID, PlayerId.GAIA)
         .modify_attribute(ObjectAttribute.HIT_POINTS, Operation.SET, 0)
         .modify_attribute(ObjectAttribute.STANDING_GRAPHIC, Operation.SET, 0)
         .modify_attribute(ObjectAttribute.WALKING_GRAPHIC, Operation.SET, 0)
         .modify_attribute(ObjectAttribute.DYING_GRAPHIC, Operation.SET, 3524)
         .create_triggers()
         )

        (UnitModifier(self.scenario, UnitInfo.HORSE_A.ID, PlayerId.THREE)
         .modify_attribute(ObjectAttribute.UNIT_SIZE_X, Operation.SET, 0)
         .modify_attribute(ObjectAttribute.UNIT_SIZE_Y, Operation.SET, 0)
         .modify_attribute(ObjectAttribute.UNIT_SIZE_Z, Operation.SET, 0)
         .modify_attribute(ObjectAttribute.STANDING_GRAPHIC, Operation.SET, 0)
         .modify_attribute(ObjectAttribute.WALKING_GRAPHIC, Operation.SET, 0)
         .create_triggers()
         )

        (UnitModifier(self.scenario, UnitInfo.CHAKRAM_THROWER.ID, PlayerId.THREE)
         .modify_attribute(ObjectAttribute.UNIT_SIZE_X, Operation.SET, 0)
         .modify_attribute(ObjectAttribute.UNIT_SIZE_Y, Operation.SET, 0)
         .modify_attribute(ObjectAttribute.UNIT_SIZE_Z, Operation.SET, 0)
         .modify_attribute(ObjectAttribute.STANDING_GRAPHIC, Operation.SET, 0)
         .modify_attribute(ObjectAttribute.WALKING_GRAPHIC, Operation.SET, 0)
         .modify_attribute(ObjectAttribute.ATTACK_GRAPHIC, Operation.SET, 0)
         .modify_attribute(ObjectAttribute.DYING_GRAPHIC, Operation.SET, 0)
         .modify_attribute(ObjectAttribute.COMBAT_ABILITY, Operation.SET, CombatAbility.ATTACK_GROUND)
         .modify_attribute(ObjectAttribute.TERRAIN_RESTRICTION_ID, Operation.SET, TerrainRestrictions.ALL)
         .modify_attribute(ObjectAttribute.ATTACK_RELOAD_TIME, Operation.SET, self.tsunami_wave_delay)
         .modify_attribute(ObjectAttribute.FRAME_DELAY, Operation.SET, 0)
         .modify_attribute(ObjectAttribute.MAX_RANGE, Operation.SET, 300)
         .modify_attribute(ObjectAttribute.ATTACK, Operation.SET, self.tsunami_unit_damage, DamageClass.BASE_MELEE)
         .modify_attribute(ObjectAttribute.ATTACK, Operation.SET, 0, DamageClass.EAGLE_WARRIORS)
         .modify_attribute(ObjectAttribute.ATTACK, Operation.SET, self.tsunami_building_damage, DamageClass.STANDARD_BUILDINGS)
         .create_triggers()
         )

        (UnitModifier(self.scenario, ProjectileInfo.CHAKRAM.ID, PlayerId.THREE)
         .modify_attribute(ObjectAttribute.STANDING_GRAPHIC, Operation.SET, 7569)
         .modify_attribute(ObjectAttribute.PROJECTILE_HIT_MODE, Operation.SET, ProjectileHitMode.ANY_OBSTACLE)
         .modify_attribute(ObjectAttribute.TERRAIN_RESTRICTION_ID, Operation.SET, TerrainRestrictions.ALL_EXCEPT_WATER_BRIDGE_CANNON)
         .modify_attribute(ObjectAttribute.MOVEMENT_SPEED, Operation.SET, self.tsunami_speed)
         .modify_attribute(ObjectAttribute.UNIT_SIZE_X, Operation.SET, 1)
         .modify_attribute(ObjectAttribute.UNIT_SIZE_X, Operation.DIVIDE, 2)
         .modify_attribute(ObjectAttribute.UNIT_SIZE_Y, Operation.SET, 1)
         .modify_attribute(ObjectAttribute.UNIT_SIZE_Y, Operation.DIVIDE, 2)
         .create_triggers()
         )

    def stop_waves_on_elevation(self):
        slopes = set()
        for tile in self.scenario.new.area().select_entire_map().to_coords(as_terrain=True):
            if tile.elevation == 1:
                for dx, dy in itertools.product((-1, 0, 1), repeat=2):
                    if (dx == 0 and dy == 0) or not (0 <= tile.x + dx < self.map_manager.map_width) or not (0 <= tile.y + dy < self.map_manager.map_height):
                        continue
                    new_tile = self.map_manager.get_tile(tile.x + dx, tile.y + dy)
                    if new_tile not in slopes and new_tile.elevation == 0:
                        slopes.add(new_tile)
                        stop_waves_on_elevation = self.trigger_manager.add_trigger("Stop Waves On Elevation", enabled=True, looping=True)
                        stop_waves_on_elevation.new_condition.objects_in_area(
                            source_player=PlayerId.THREE,
                            area_x1=new_tile.x,
                            area_y1=new_tile.y,
                            area_x2=new_tile.x,
                            area_y2=new_tile.y,
                            quantity=1
                        )
                        stop_waves_on_elevation.new_effect.create_object(
                            source_player=PlayerId.GAIA,
                            object_list_unit_id=UnitInfo.VULTURE.ID,
                            location_x=new_tile.x,
                            location_y=new_tile.y
                        )
                        stop_waves_on_elevation.new_effect.kill_object(
                            source_player=PlayerId.THREE,
                            area_x1=new_tile.x,
                            area_y1=new_tile.y,
                            area_x2=new_tile.x,
                            area_y2=new_tile.y
                        )
            if tile.elevation >= 1:
                stop_waves_on_elevation = self.trigger_manager.add_trigger("Stop Waves On Elevation", enabled=True, looping=True)
                stop_waves_on_elevation.new_condition.objects_in_area(
                    source_player=PlayerId.THREE,
                    area_x1=tile.x,
                    area_y1=tile.y,
                    area_x2=tile.x,
                    area_y2=tile.y,
                    quantity=1
                )
                stop_waves_on_elevation.new_effect.create_object(
                    source_player=PlayerId.GAIA,
                    object_list_unit_id=UnitInfo.VULTURE.ID,
                    location_x=tile.x,
                    location_y=tile.y
                )
                stop_waves_on_elevation.new_effect.kill_object(
                    source_player=PlayerId.THREE,
                    area_x1=tile.x,
                    area_y1=tile.y,
                    area_x2=tile.x,
                    area_y2=tile.y
                )

    def generate_tsunami_trigger(self, tile1: Tile, tile2: Tile, amplitude: int):
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
        wave_rect = [(x, y) for x in range(0, int(distance)) for y in range(0, amplitude + 10) if wave_list[x] - 1.5 < y < wave_list[x] + 1.5]
        wave_tiles = [transformations.get_tile(transformations.rotate_and_translate_tile(tile, rot_angle, (tile1.x, tile1.y))) for tile in wave_rect]
        create_units = self.trigger_manager.add_trigger("Create Units", enabled=False, looping=False)
        attack_ground = self.trigger_manager.add_trigger("Attack Ground", enabled=False, looping=False)
        for tile in wave_tiles:
            x, y = tile
            while 0 <= x < self.map_manager.map_width and 0 <= y < self.map_manager.map_height:
                x += perpendicular[0]
                y += perpendicular[1]
            x = int(x - perpendicular[0])
            y = int(y - perpendicular[1])
            attack_ground.new_effect.task_object(
                object_list_unit_id=UnitInfo.CHAKRAM_THROWER.ID,
                location_x=x,
                location_y=y,
                area_x1=tile.x,
                area_x2=tile.x,
                area_y1=tile.y,
                area_y2=tile.y,
                source_player=PlayerId.THREE,
                action_type=ActionType.ATTACK_GROUND
            )
            create_units.new_effect.create_object(
                source_player=PlayerId.THREE,
                object_list_unit_id=UnitInfo.CHAKRAM_THROWER.ID,
                location_x=tile.x,
                location_y=tile.y
            )
        create_units.new_effect.change_object_stance(
            source_player=PlayerId.THREE,
            object_list_unit_id=UnitInfo.CHAKRAM_THROWER.ID,
            attack_stance=AttackStance.NO_ATTACK_STANCE
        )
        create_units.new_effect.disable_unit_targeting(
            source_player=PlayerId.THREE,
            object_list_unit_id=UnitInfo.CHAKRAM_THROWER.ID
        )
        create_units.new_effect.disable_object_selection(
            source_player=PlayerId.THREE,
            object_list_unit_id=UnitInfo.CHAKRAM_THROWER.ID
        )
        create_units.new_effect.activate_trigger(
            trigger_id=attack_ground.trigger_id
        )
        attack_ground.new_effect.activate_trigger(
            trigger_id=self.quit_units.trigger_id
        )
        first_wave = self.trigger_manager.add_trigger("First Wave", enabled=False)
        second_wave = self.trigger_manager.add_trigger("Second Wave", enabled=False)
        third_wave = self.trigger_manager.add_trigger("Third Wave", enabled=False)
        first_wave.new_effect.activate_trigger(create_units.trigger_id)
        first_wave.new_effect.activate_trigger(second_wave.trigger_id)
        first_wave.new_effect.activate_trigger(third_wave.trigger_id)
        for player in self.player_list:
            first_wave.new_effect.play_sound(
                source_player=player,
                sound_name=self.tsunami_sound
            )
        second_wave.new_condition.timer(self.tsunami_wave_delay)
        second_wave.new_effect.activate_trigger(create_units.trigger_id)
        third_wave.new_condition.timer(self.tsunami_wave_delay * 2)
        third_wave.new_effect.activate_trigger(create_units.trigger_id)
        return first_wave

    def create_tsunamis(self):
        left_tsunami = self.generate_tsunami_trigger(self.left_tsunami[0], self.left_tsunami[1], 8)
        right_tsunami = self.generate_tsunami_trigger(self.right_tsunami[0], self.right_tsunami[1], 8)
        diagonal_tsunami = self.generate_tsunami_trigger(self.diagonal_tsunami[0], self.diagonal_tsunami[1], 8)

        lateral_tsunami = self.trigger_manager.add_trigger("Lateral Tsunami", enabled=False)
        lateral_tsunami.new_effect.activate_trigger(left_tsunami.trigger_id)
        lateral_tsunami.new_effect.activate_trigger(right_tsunami.trigger_id)

        tsunami_manager = self.trigger_manager.add_trigger("Tsunami Manager", enabled=False)
        activate_lateral_tsunami = self.trigger_manager.add_trigger("Activate Lateral Tsunami", enabled=False)
        activate_diagonal_tsunami = self.trigger_manager.add_trigger("Activate Lateral Tsunami", enabled=False)

        tsunami_manager.new_effect.activate_trigger(activate_lateral_tsunami.trigger_id)
        tsunami_manager.new_effect.activate_trigger(activate_diagonal_tsunami.trigger_id)

        activate_lateral_tsunami.new_condition.variable_value(variable=0, comparison=Comparison.EQUAL, quantity=0)
        activate_lateral_tsunami.new_effect.activate_trigger(lateral_tsunami.trigger_id)
        activate_lateral_tsunami.new_effect.deactivate_trigger(activate_diagonal_tsunami.trigger_id)
        activate_lateral_tsunami.new_effect.change_variable(variable=0, quantity=1)

        activate_diagonal_tsunami.new_condition.variable_value(variable=0, comparison=Comparison.EQUAL,quantity=1)
        activate_diagonal_tsunami.new_effect.activate_trigger(diagonal_tsunami.trigger_id)
        activate_diagonal_tsunami.new_effect.deactivate_trigger(activate_lateral_tsunami.trigger_id)
        activate_diagonal_tsunami.new_effect.change_variable(variable=0, quantity=0)

        period_triggers = [self.trigger_manager.add_trigger(f"Period Trigger {i}", enabled=False) for i, _ in enumerate(self.tsunami_periods)]
        for i, trigger in enumerate(period_triggers):
            trigger.new_condition.timer(self.tsunami_periods[i])
            trigger.new_effect.activate_trigger(tsunami_manager.trigger_id)
        random_period = EqualRandomProbability(self.trigger_manager, period_triggers, "Random Period")
        tsunami_manager.new_effect.activate_trigger(random_period.enable_probability_trigger.trigger_id)

        initial_tsunami_delay = self.trigger_manager.add_trigger("Initial Tsunami Delay", enabled=True)
        initial_tsunami_delay.new_condition.timer(self.tsunami_initial_delay)
        initial_tsunami_delay.new_effect.activate_trigger(tsunami_manager.trigger_id)


if __name__ == "__main__":
    tsunami = Tsunami2(
        input_scenario_name='Tsunami 2 Fukushima',
        output_scenario_name='Tsunami 2 Fukushima_output'
    )
    tsunami.convert()
