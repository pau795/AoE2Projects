from pathlib import Path

from AoE2ScenarioParser.datasets.buildings import BuildingInfo
from AoE2ScenarioParser.datasets.other import OtherInfo
from AoE2ScenarioParser.datasets.players import PlayerId
from AoE2ScenarioParser.datasets.trigger_lists import ActionType, AttackStance
from AoE2ScenarioParser.datasets.units import UnitInfo
from AoE2ScenarioParser.objects.data_objects.trigger import Trigger
from AoE2ScenarioParser.objects.data_objects.unit import Unit
from AoE2ScenarioParser.objects.support.area import Area
from AoE2ScenarioParser.objects.support.tile import Tile
from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario

from scenarios.lib import utils


class BridgeFactory:
    VERTICAL_MOBILE_BRIDGE_PIECE_UNIT = UnitInfo.SKIRMISHER.ID
    HORIZONTAL_MOBILE_BRIDGE_PIECE_UNIT = UnitInfo.ELITE_SKIRMISHER.ID
    VERTICAL_MOBILE_BRIDGE_WALL_UNIT = UnitInfo.SPEARMAN.ID
    HORIZONTAL_MOBILE_BRIDGE_WALL_UNIT = UnitInfo.PIKEMAN.ID
    VERTICAL_FIXED_BRIDGE_PIECE_UNIT = BuildingInfo.WOODEN_BRIDGE_A_MIDDLE.ID
    HORIZONTAL_FIXED_BRIDGE_PIECE_UNIT = BuildingInfo.WOODEN_BRIDGE_B_MIDDLE.ID
    VERTICAL_FIXED_BRIDGE_WALL_UNIT = BuildingInfo.FENCE.ID
    HORIZONTAL_FIXED_BRIDGE_WALL_UNIT = BuildingInfo.PALISADE_WALL.ID
    VERTICAL_INTERMEDIATE_BRIDGE_WALL_UNIT = OtherInfo.FLAG_C.ID
    HORIZONTAL_INTERMEDIATE_BRIDGE_WALL_UNIT = OtherInfo.FLAG_D.ID

    def __init__(self, scenario: AoE2DEScenario, player_list):
        self.scenario = scenario
        self.trigger_manager = scenario.trigger_manager
        self.map_manager = scenario.map_manager
        self.xs_manager = scenario.xs_manager
        self.player_list = player_list
        self.bridge_sound = "bridge_deploy"

    def initial_bridges(self, bridge_number: int, intermediate_bridge_area: Area, gates: list[Unit]):
        remove_bridges = self.trigger_manager.add_trigger(f'Bridge {bridge_number} remove', enabled=True)
        remove_bridges.new_effect.remove_object(
            source_player=PlayerId.THREE,
            area_x1=intermediate_bridge_area.x1,
            area_y1=intermediate_bridge_area.y1,
            area_x2=intermediate_bridge_area.x2,
            area_y2=intermediate_bridge_area.y2
        )
        lock_gates = self.trigger_manager.add_trigger(f'Bridge {bridge_number} lock gates', enabled=True)
        for gate in gates:
            lock_gates.new_effect.lock_gate(
                selected_object_ids=gate.reference_id
            )

    def generate_moving_stuff(self, name: str,  create: bool, init_tile: Tile, end_tile: Tile, moving_unit: int, fixed_unit: int, intermediate_unit: int = None):
        direction = utils.get_direction(init_tile, end_tile)
        create_moving_unit_trigger = self.trigger_manager.add_trigger(f'{name} create moving unit ', enabled=False)
        create_moving_unit_trigger.new_effect.create_object(
            object_list_unit_id=moving_unit,
            source_player=PlayerId.THREE,
            location_x=init_tile.x,
            location_y=init_tile.y
        )
        destination = utils.get_edge_tile(self.map_manager, init_tile, direction)
        create_moving_unit_trigger.new_effect.task_object(
            object_list_unit_id=moving_unit,
            source_player=PlayerId.THREE,
            area_x1=init_tile.x,
            area_y1=init_tile.y,
            area_x2=init_tile.x,
            area_y2=init_tile.y,
            location_x=destination.x,
            location_y=destination.y,
            action_type=ActionType.MOVE
        )
        create_moving_unit_trigger.new_effect.disable_unit_targeting(
            source_player=PlayerId.THREE,
            object_list_unit_id=moving_unit,
            area_x1=init_tile.x,
            area_y1=init_tile.y,
            area_x2=init_tile.x,
            area_y2=init_tile.y
        )
        create_moving_unit_trigger.new_effect.change_object_stance(
            source_player=PlayerId.THREE,
            object_list_unit_id=moving_unit,
            area_x1=init_tile.x,
            area_y1=init_tile.y,
            area_x2=init_tile.x,
            area_y2=init_tile.y,
            attack_stance=AttackStance.NO_ATTACK_STANCE
        )
        remove_moving_trigger = self.trigger_manager.add_trigger(f'{name} remove moving unit', enabled=False)
        remove_moving_trigger.new_condition.objects_in_area(
            source_player=PlayerId.THREE,
            object_list=moving_unit,
            quantity=1,
            area_x1=end_tile.x,
            area_y1=end_tile.y,
            area_x2=end_tile.x,
            area_y2=end_tile.y,
        )
        remove_moving_trigger.new_effect.remove_object(
            object_list_unit_id=moving_unit,
            source_player=PlayerId.THREE,
            area_x1=end_tile.x,
            area_y1=end_tile.y,
            area_x2=end_tile.x,
            area_y2=end_tile.y,
        )
        create_moving_unit_trigger.new_effect.activate_trigger(remove_moving_trigger.trigger_id)
        step = 0
        fixed_units_triggers = []
        pass_tile = Tile(init_tile.x + direction[0], init_tile.y + direction[1])
        end_pass_tile = Tile(end_tile.x, end_tile.y)

        while pass_tile != end_pass_tile:
            create_fixed_unit_trigger = self.trigger_manager.add_trigger(f'{name} {"create" if create else "remove"} fixed unit {step}', enabled=False)
            create_fixed_unit_trigger.new_condition.objects_in_area(
                source_player=PlayerId.THREE,
                area_x1=pass_tile.x,
                area_y1=pass_tile.y,
                area_x2=pass_tile.x,
                area_y2=pass_tile.y,
                object_list=moving_unit,
                quantity=1
            )
            if create:
                if intermediate_unit is not None:
                    create_fixed_unit_trigger.new_effect.create_object(
                        object_list_unit_id=intermediate_unit,
                        source_player=PlayerId.THREE,
                        location_x=pass_tile.x,
                        location_y=pass_tile.y
                    )
                    create_fixed_unit_trigger.new_effect.replace_object(
                        source_player=PlayerId.THREE,
                        target_player=PlayerId.THREE,
                        object_list_unit_id=intermediate_unit,
                        object_list_unit_id_2=fixed_unit,
                        area_x1=pass_tile.x,
                        area_y1=pass_tile.y,
                        area_x2=pass_tile.x,
                        area_y2=pass_tile.y
                    )
                else:
                    create_fixed_unit_trigger.new_effect.create_object(
                        object_list_unit_id=fixed_unit,
                        source_player=PlayerId.THREE,
                        location_x=pass_tile.x,
                        location_y=pass_tile.y
                    )
            else:
                create_fixed_unit_trigger.new_effect.remove_object(
                    object_list_unit_id=fixed_unit,
                    source_player=PlayerId.THREE,
                    area_x1=pass_tile.x,
                    area_y1=pass_tile.y,
                    area_x2=pass_tile.x,
                    area_y2=pass_tile.y
                )
            for player in self.player_list:
                create_fixed_unit_trigger.new_effect.kill_object(
                    source_player=player,
                    area_x1=pass_tile.x,
                    area_y1=pass_tile.y,
                    area_x2=pass_tile.x,
                    area_y2=pass_tile.y,
                )
            fixed_units_triggers.append(create_fixed_unit_trigger)
            pass_tile = Tile(pass_tile.x + direction[0], pass_tile.y + direction[1])
            step += 1
        for trigger in fixed_units_triggers:
            create_moving_unit_trigger.new_effect.activate_trigger(trigger_id=trigger.trigger_id)
        return create_moving_unit_trigger

    def generate_retractable_bridges(self, bridge_area_list: list[list[Area]], gate_list: list[list[Unit]]) -> list[tuple[Trigger, Trigger]]:
        bridge_triggers = []
        for i, (areas, gates) in enumerate(zip(bridge_area_list, gate_list)):

            init_area = areas[0]
            end_area = areas[1]
            is_area_horizontal = init_area.get_width() > init_area.get_height()
            bridge_area = Area.from_tiles(init_area.corner1, end_area.corner2)
            intermediate_bridge_area = bridge_area.copy()
            intermediate_bridge_area.shrink(1)
            intermediate_bridge_area = utils.modify_area_dimension(intermediate_bridge_area, 'long', 'shrink', 1)
            self.initial_bridges(i, intermediate_bridge_area, gates)

            moving_bridge_piece_unit = self.HORIZONTAL_MOBILE_BRIDGE_PIECE_UNIT if is_area_horizontal else self.VERTICAL_MOBILE_BRIDGE_PIECE_UNIT
            fixed_bridge_piece_umit = self.HORIZONTAL_FIXED_BRIDGE_PIECE_UNIT if is_area_horizontal else self.VERTICAL_FIXED_BRIDGE_PIECE_UNIT
            moving_bridge_wall_unit = self.HORIZONTAL_MOBILE_BRIDGE_WALL_UNIT if is_area_horizontal else self.VERTICAL_MOBILE_BRIDGE_WALL_UNIT
            fixed_bridge_wall_unit = self.HORIZONTAL_FIXED_BRIDGE_WALL_UNIT if is_area_horizontal else self.VERTICAL_FIXED_BRIDGE_WALL_UNIT
            intermediate_bridge_wall_unit = self.HORIZONTAL_INTERMEDIATE_BRIDGE_WALL_UNIT if is_area_horizontal else self.VERTICAL_INTERMEDIATE_BRIDGE_WALL_UNIT
            direction = utils.get_direction(init_area.corner1, end_area.corner1)

            init_bridge_area = init_area.copy()
            init_bridge_area = utils.modify_area_dimension(init_bridge_area, "long", "shrink", 1)
            init_bridge_area.move(direction[0], direction[1])

            end_bridge_area = end_area.copy()
            end_bridge_area = utils.modify_area_dimension(end_bridge_area, "long", "shrink", 1)
            end_bridge_area.move(-direction[0], -direction[1])

            deploy_bridge_trigger = self.trigger_manager.add_trigger(f"Deploy bridge {i}", enabled=False)
            deploy_lines_delay_trigger = self.trigger_manager.add_trigger(f"Deploy bridge {i} lines delay", enabled=False)
            retract_bridge_trigger = self.trigger_manager.add_trigger(f"Retract bridge {i}", enabled=False)
            retract_lines_delay_trigger = self.trigger_manager.add_trigger(f"Retract bridge {i} lines delay", enabled=False)

            deploy_lines_delay_trigger.new_condition.timer(2)
            retract_lines_delay_trigger.new_condition.timer(2)

            deploy_bridge_trigger.new_effect.activate_trigger(deploy_lines_delay_trigger.trigger_id)
            retract_bridge_trigger.new_effect.activate_trigger(retract_lines_delay_trigger.trigger_id)

            for trigger in [deploy_bridge_trigger, retract_bridge_trigger]:
                for player in self.player_list:
                    trigger.new_effect.play_sound(
                        source_player=player,
                        sound_name=self.bridge_sound,
                        location_x=int(bridge_area.get_center()[0]),
                        location_y=int(bridge_area.get_center()[1])
                    )
            for gate in gates:
                deploy_bridge_trigger.new_effect.unlock_gate(selected_object_ids=gate.reference_id)
                retract_bridge_trigger.new_effect.lock_gate(selected_object_ids=gate.reference_id)

            for j, (init_tile, end_tile) in enumerate(zip([init_area.corner1, init_area.corner2], [end_area.corner1, end_area.corner2])):
                deploy_bridge_wall = self.generate_moving_stuff(f"Deploy bridge {i} wall {j}", True, init_tile, end_tile, moving_bridge_wall_unit, fixed_bridge_wall_unit, intermediate_bridge_wall_unit)
                retract_bridge_wall = self.generate_moving_stuff(f"Retract bridge {i} wall {j}", False, end_tile, init_tile, moving_bridge_wall_unit, fixed_bridge_wall_unit)
                deploy_bridge_trigger.new_effect.activate_trigger(deploy_bridge_wall.trigger_id)
                retract_bridge_trigger.new_effect.activate_trigger(retract_bridge_wall.trigger_id)
            for j, (init_tile, end_tile) in enumerate(zip(init_bridge_area.to_coords(), end_bridge_area.to_coords())):
                deploy_bridge_piece = self.generate_moving_stuff(f"Deploy bridge {i} line {j}", True, init_tile, end_tile, moving_bridge_piece_unit, fixed_bridge_piece_umit)
                retract_bridge_piece = self.generate_moving_stuff(f"Retract bridge {i} line {j}", False, end_tile, init_tile, moving_bridge_piece_unit, fixed_bridge_piece_umit)
                deploy_lines_delay_trigger.new_effect.activate_trigger(deploy_bridge_piece.trigger_id)
                retract_lines_delay_trigger.new_effect.activate_trigger(retract_bridge_piece.trigger_id)
            bridge_triggers.append((deploy_bridge_trigger, retract_bridge_trigger))

        return bridge_triggers

    def set_bridge_stats(self):
        module_dir = Path(__file__).parent
        xs_file = module_dir / "xs/bridge_stats.xs"
        self.xs_manager.add_script(xs_file_path=str(xs_file))
        xs_trigger = self.trigger_manager.add_trigger("XS CALL BRIDGE_STATS")
        xs_trigger.new_effect.script_call(message="bridge_stats();")
