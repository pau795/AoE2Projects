import math

from AoE2ScenarioParser.datasets.buildings import BuildingInfo
from AoE2ScenarioParser.datasets.players import PlayerId
from AoE2ScenarioParser.datasets.terrains import TerrainId
from AoE2ScenarioParser.datasets.trigger_lists import ObjectState, AttackStance, Operation
from AoE2ScenarioParser.datasets.units import UnitInfo
from AoE2ScenarioParser.objects.support.area import Area

from scenarios.lib.bridge_factory import BridgeFactory
from scenarios.lib.cave_factory import CaveFactory
from scenarios.lib.civ_settings import CivSettings
from scenarios.lib.equally_probable_trigger_list import EquallyProbableTriggerList
from scenarios.lib.parser_project import ParserProject


class Alcatraz(ParserProject):
    MOBILE_CITY_WALL_UNIT = UnitInfo.SCOUT_CAVALRY.ID
    MOBILE_FORTIFIED_PALISADE_WALL_UNIT = UnitInfo.LIGHT_CAVALRY.ID
    MOBILE_SEA_WALL_UNIT = UnitInfo.HUSSAR.ID

    SEA_WALL = BuildingInfo.SEA_WALL.ID
    CITY_WALL = BuildingInfo.CITY_WALL.ID
    FORTIFIED_PALISADE_WALL = BuildingInfo.FORTIFIED_PALISADE_WALL.ID

    def __init__(self, input_scenario_name: str, output_scenario_name: str):
        super().__init__(input_scenario_name, output_scenario_name)
        self.trigger_manager = self.scenario.trigger_manager
        self.data_triggers = self.scenario.actions.load_data_triggers()
        self.map_manager = self.scenario.map_manager
        self.unit_manager = self.scenario.unit_manager
        self.xs_manager = self.scenario.xs_manager
        self.player_list = [PlayerId.ONE, PlayerId.TWO]
        self.initial_bridge_delay = 600
        self.bridge_period = 150
        self.wall_period = 150
        self.bridge_probability = 50
        self.building_speed = 0.5
        self.moving_wall_sound = "moving_wall"

    def get_wall_info(self, i) -> tuple[int, int, int]:
        if 1 <= i <= 4:
            return 600, self.CITY_WALL, self.MOBILE_CITY_WALL_UNIT
        elif 5 <= i <= 6:
            return 450, self.CITY_WALL, self.MOBILE_CITY_WALL_UNIT
        elif 7 <= i <= 9:
            return 450, self.FORTIFIED_PALISADE_WALL, self.MOBILE_FORTIFIED_PALISADE_WALL_UNIT
        elif 10 <= i <= 11:
            return 750, self.SEA_WALL, self.MOBILE_SEA_WALL_UNIT
        else:
            return 1, 0, 0

    def initial_settings(self):
        horse_targeting = self.trigger_manager.add_trigger("Disable Horse Targeting", enabled=True)
        horse_targeting.new_effect.disable_unit_targeting(source_player=PlayerId.THREE, object_list_unit_id=UnitInfo.HORSE_A.ID)
        initial_sounds = self.trigger_manager.add_trigger("Initial Sounds", enabled=True)
        for player in self.player_list:
            player_defeat = self.trigger_manager.add_trigger(f"Defeat player {player}", enabled=True)
            player_defeat.new_condition.player_defeated(source_player=player)
            player_defeat.new_effect.declare_victory(source_player=PlayerId.THREE, enabled=False)
            initial_sounds.new_effect.play_sound(sound_name="introcastillo", source_player=player)

    def setup_bridges(self):
        initial_variables = self.trigger_manager.add_trigger("Initial Bridge Variables", enabled=True)
        initial_variables.new_effect.change_variable(message="Bridge Pack 0", variable=0, quantity=0, operation=Operation.SET)
        initial_variables.new_effect.change_variable(message="Bridge Pack 1", variable=1, quantity=0, operation=Operation.SET)
        initial_variables.new_effect.change_variable(message="Bridge Pack 2", variable=2, quantity=0, operation=Operation.SET)
        bridge_factory = BridgeFactory(self.scenario, self.player_list)
        bridge_factory.set_bridge_stats()
        bridge_areas = self.data_triggers.areas['bridge']
        center_tile = self.data_triggers.tiles['fortress_center'][0]
        bridge_triggers = bridge_factory.generate_retractable_bridges(bridge_areas, center_tile)
        bridge_packs = [(bridge_triggers[0], bridge_triggers[5]), (bridge_triggers[1], bridge_triggers[4]), (bridge_triggers[2], bridge_triggers[3])]
        initial_deploy_delay = self.trigger_manager.add_trigger(f'Initial Bridge deploy delay', enabled=True)
        initial_deploy_delay.new_condition.timer(timer=self.initial_bridge_delay)
        deploy_delay = self.trigger_manager.add_trigger(f'Bridge deploy delay', enabled=False)
        retract_delay = self.trigger_manager.add_trigger(f'Bridge retract delay', enabled=False)
        deploy_delay.new_condition.timer(timer=self.bridge_period)
        retract_delay.new_condition.timer(timer=self.bridge_period)
        deploy_pack_triggers = []
        retract_pack_triggers = []
        for i, bridge_pack in enumerate(bridge_packs):
            trigger_pack_deploy = self.trigger_manager.add_trigger(f'Bridge pack {i} deploy', enabled=False)
            trigger_pack_retract = self.trigger_manager.add_trigger(f'Bridge pack {i} retract', enabled=False)
            trigger_pack_retract.new_condition.variable_value(variable=i, quantity=1)
            trigger_pack_retract.new_effect.change_variable(variable=i, quantity=0, operation=Operation.SET)
            trigger_pack_deploy.new_effect.change_variable(variable=i, quantity=1, operation=Operation.SET)
            trigger_pack_deploy.new_effect.activate_trigger(retract_delay.trigger_id)
            trigger_pack_retract.new_effect.activate_trigger(deploy_delay.trigger_id)
            for deploy_bridge_trigger, retract_bridge_trigger in bridge_pack:
                trigger_pack_deploy.new_effect.activate_trigger(deploy_bridge_trigger.trigger_id)
                trigger_pack_retract.new_effect.activate_trigger(retract_bridge_trigger.trigger_id)
            deploy_pack_triggers.append(trigger_pack_deploy)
            retract_pack_triggers.append(trigger_pack_retract)
        for trigger in retract_pack_triggers:
            for trigger2 in retract_pack_triggers:
                if trigger != trigger2:
                    trigger.new_effect.deactivate_trigger(trigger2.trigger_id)
            retract_delay.new_effect.activate_trigger(trigger.trigger_id)
        random_deploy = EquallyProbableTriggerList(self.trigger_manager, deploy_pack_triggers, "Random deploy bridge pack")
        deploy_delay.new_effect.activate_trigger(random_deploy.enable_probability_trigger.trigger_id)
        initial_deploy_delay.new_effect.activate_trigger(random_deploy.enable_probability_trigger.trigger_id)

    def setup_caves(self):
        for tile in self.scenario.new.area().select_entire_map().to_coords(as_terrain=True):
            if tile.terrain_id == TerrainId.BLACK:
                tile.terrain_id = TerrainId.CORRUPTION
        cave_list = [v for k, v in self.data_triggers.areas.items() if k.startswith('cave')]
        cave_factory = CaveFactory(self.scenario, self.player_list)
        cave_factory.caves_stats()
        cave_factory.generate_caves(cave_list)

    def setup_walls(self):
        self.xs_manager.add_script("alcatraz.xs")
        xs_trigger = self.trigger_manager.add_trigger("XS CALL WALL_STATS")
        xs_trigger.new_effect.script_call(message="wall_stats();")
        wall_areas = {k: v for k, v in self.data_triggers.areas.items() if k.startswith('muro')}
        for i, (key, areas) in enumerate(wall_areas.items()):
            print(i, key, areas[0].get_dimensions(), areas[1].get_dimensions())
            delay, fixed_unit, mobile_unit = self.get_wall_info(i + 1)
            first_way = self.move_walls(areas[0], areas[1], mobile_unit, fixed_unit)
            second_way = self.move_walls(areas[1], areas[0], mobile_unit, fixed_unit)
            first_way.new_effect.activate_trigger(second_way.trigger_id)
            second_way.new_effect.activate_trigger(first_way.trigger_id)
            initial_forest_delay = self.trigger_manager.add_trigger(f'{key} initial wall delay', enabled=True)
            initial_forest_delay.new_condition.timer(delay)
            initial_forest_delay.new_effect.activate_trigger(first_way.trigger_id)

    def move_walls(self, source_area: Area, target_area: Area, mobile_wall_unit: int, fixed_wall_unit: int):
        source_tiles = source_area.to_coords()
        target_tiles = target_area.to_coords()
        walls_phase_1 = self.trigger_manager.add_trigger(f"Remove Walls, Create Mobile Units, Move Them", enabled=False)
        trees_phase_2 = self.trigger_manager.add_trigger(f"Check for Mobile Units, Remove Mobile Units, Create Walls", enabled=False)
        walls_phase_1.new_condition.timer(self.wall_period)
        walls_phase_1.new_effect.remove_object(
            object_list_unit_id=fixed_wall_unit,
            source_player=PlayerId.THREE,
            object_state=ObjectState.ALIVE,
            area_x1=source_area.x1,
            area_y1=source_area.y1,
            area_x2=source_area.x2,
            area_y2=source_area.y2
        )
        for source_tile in source_tiles:
            walls_phase_1.new_effect.create_object(
                object_list_unit_id=mobile_wall_unit,
                source_player=PlayerId.THREE,
                location_x=source_tile.x,
                location_y=source_tile.y
            )
        walls_phase_1.new_effect.change_object_stance(
            object_list_unit_id=mobile_wall_unit,
            source_player=PlayerId.THREE,
            area_x1=source_area.x1,
            area_y1=source_area.y1,
            area_x2=source_area.x2,
            area_y2=source_area.y2,
            attack_stance=AttackStance.NO_ATTACK_STANCE
        )

        walls_phase_1.new_effect.disable_object_selection(
            object_list_unit_id=mobile_wall_unit,
            source_player=PlayerId.THREE,
            area_x1=source_area.x1,
            area_y1=source_area.y1,
            area_x2=source_area.x2,
            area_y2=source_area.y2
        )
        walls_phase_1.new_effect.disable_unit_targeting(
            object_list_unit_id=mobile_wall_unit,
            source_player=PlayerId.THREE,
            area_x1=source_area.x1,
            area_y1=source_area.y1,
            area_x2=source_area.x2,
            area_y2=source_area.y2
        )
        for i, source_tile in enumerate(source_tiles):
            walls_phase_1.new_effect.task_object(
                object_list_unit_id=mobile_wall_unit,
                source_player=PlayerId.THREE,
                area_x1=source_tile.x,
                area_y1=source_tile.y,
                area_x2=source_tile.x,
                area_y2=source_tile.y,
                location_x=target_tiles[i].x,
                location_y=target_tiles[i].y
            )
        for player in self.player_list:
            walls_phase_1.new_effect.play_sound(
                sound_name=self.moving_wall_sound,
                source_player=player,
                location_x=int(source_area.get_center()[0]),
                location_y=int(source_area.get_center()[1])

            )
        walls_phase_1.new_effect.activate_trigger(trigger_id=trees_phase_2.trigger_id)

        # PHASE 2
        rotation = source_area.get_width() != target_area.get_width()
        distance = math.dist(source_area.get_center(), target_area.get_center())
        timer = int(math.ceil(distance / self.building_speed) + (4 * (2.3 if rotation else 1))) + 1
        trees_phase_2.new_condition.timer(timer=timer)

        trees_phase_2.new_effect.remove_object(
            object_list_unit_id=mobile_wall_unit,
            source_player=PlayerId.THREE,
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
                object_list_unit_id=mobile_wall_unit,
                source_player=PlayerId.THREE,
                location_x=target_tile.x,
                location_y=target_tile.y
            )
        trees_phase_2.new_effect.replace_object(
            object_list_unit_id=mobile_wall_unit,
            object_list_unit_id_2=fixed_wall_unit,
            source_player=PlayerId.THREE,
            target_player=PlayerId.THREE,
            area_x1=max(0, target_area.x1 - 1),
            area_y1=max(0, target_area.y1 - 1),
            area_x2=min(self.scenario.map_manager.map_width - 1, target_area.x2 + 1),
            area_y2=min(self.scenario.map_manager.map_height - 1, target_area.y2 + 1)
        )
        return walls_phase_1

    def process(self):
        CivSettings(self.scenario, self.player_list)
        self.initial_settings()
        self.setup_bridges()
        self.setup_caves()
        self.setup_walls()


if __name__ == '__main__':
    alcatraz_class = Alcatraz(
        input_scenario_name=f'alcatraz_editar',
        output_scenario_name=f'alcatraz_output'
    )
    alcatraz_class.convert()
