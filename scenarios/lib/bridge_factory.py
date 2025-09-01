from pathlib import Path

from AoE2ScenarioParser.datasets.buildings import BuildingInfo
from AoE2ScenarioParser.datasets.other import OtherInfo
from AoE2ScenarioParser.datasets.players import PlayerId
from AoE2ScenarioParser.datasets.terrains import TerrainId
from AoE2ScenarioParser.datasets.trigger_lists import ActionType, AttackStance
from AoE2ScenarioParser.datasets.units import UnitInfo
from AoE2ScenarioParser.objects.data_objects.trigger import Trigger
from AoE2ScenarioParser.objects.support.area import Area
from AoE2ScenarioParser.objects.support.tile import Tile
from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario
from scenarios.lib import utils


class BridgeFactory:
    VERTICAL_BRIDGE_UNIT = UnitInfo.SKIRMISHER.ID
    HORIZONTAL_BRIDGE_UNIT = UnitInfo.ELITE_SKIRMISHER.ID
    HORIZONTAL_CHAIN_INTERMEDIATE_UNIT = OtherInfo.FLAG_A.ID
    VERTICAL_CHAIN_INTERMEDIATE_UNIT = OtherInfo.FLAG_B.ID
    HORIZONTAL_CHAIN_FIXED_UNIT = OtherInfo.ROCK_FORMATION_1.ID
    VERTICAL_CHAIN_FIXED_UNIT = OtherInfo.ROCK_FORMATION_2.ID

    def __init__(self, scenario: AoE2DEScenario, player_list):
        self.scenario = scenario
        self.trigger_manager = scenario.trigger_manager
        self.map_manager = scenario.map_manager
        self.xs_manager = scenario.xs_manager
        self.player_list = player_list
        self.bridge_sound = "bridge_deploy"

    def initial_bridges(self, bridge_number: int,
                        init_bridge_unit: int, end_bridge_unit: int, chain_unit: int,
                        extremes_bridge_area: Area, init_extreme_bridge_area: Area, end_extreme_bridge_area: Area,
                        init_shore_area: Area, end_shore_area: Area):
        for tile1, tile2 in zip(init_shore_area.to_coords(as_terrain=True), end_shore_area.to_coords(as_terrain=True)):
            tile1.terrain_id = TerrainId.ROCK_1
            tile2.terrain_id = TerrainId.ROCK_1
        create_bridges = self.trigger_manager.add_trigger(f'Bridge {bridge_number} create', enabled=True)
        create_bridges.new_condition.timer(timer=2)
        for tile in extremes_bridge_area.to_coords(as_terrain=True):
            create_bridges.new_effect.create_object(
                object_list_unit_id=BuildingInfo.BRIDGE_PIECE_AB_MIDDLE.ID,
                source_player=PlayerId.THREE,
                location_x=tile.x,
                location_y=tile.y
            )
        remove_bridges = self.trigger_manager.add_trigger(f'Bridge {bridge_number} remove', enabled=True)
        remove_bridges.new_condition.timer(timer=3)
        remove_bridges.new_effect.remove_object(
            object_list_unit_id=BuildingInfo.BRIDGE_PIECE_AB_MIDDLE.ID,
            source_player=PlayerId.THREE,
            area_x1=extremes_bridge_area.x1,
            area_y1=extremes_bridge_area.y1,
            area_x2=extremes_bridge_area.x2,
            area_y2=extremes_bridge_area.y2
        )
        top_bottom_bridges = self.trigger_manager.add_trigger(f'Bridge {bridge_number} init and end', enabled=True)
        top_bottom_bridges.new_condition.timer(timer=4)
        for tile in init_extreme_bridge_area.to_coords(as_terrain=True):
            top_bottom_bridges.new_effect.create_object(
                object_list_unit_id=init_bridge_unit,
                source_player=PlayerId.THREE,
                location_x=tile.x,
                location_y=tile.y
            )
        for tile in end_extreme_bridge_area.to_coords(as_terrain=True):
            top_bottom_bridges.new_effect.create_object(
                object_list_unit_id=end_bridge_unit,
                source_player=PlayerId.THREE,
                location_x=tile.x,
                location_y=tile.y
            )
        for i, (init_tile, end_tile) in enumerate(zip(init_shore_area.to_coords(), end_shore_area.to_coords())):
            if i % 2 != 0:
                top_bottom_bridges.new_effect.create_object(
                    object_list_unit_id=chain_unit,
                    source_player=PlayerId.GAIA,
                    location_x=init_tile.x,
                    location_y=init_tile.y
                )
                top_bottom_bridges.new_effect.create_object(
                    object_list_unit_id=chain_unit,
                    source_player=PlayerId.GAIA,
                    location_x=end_tile.x,
                    location_y=end_tile.y
                )

    def deploy_chain(self, bridge_number: int, init_chain_tiles: list[Tile], end_chain_tiles: list[Tile], increment: tuple[int, int],
                     short_chain_unit: int, intermediate_chain_unit: int, fixed_chain_unit: int):
        chain_trigger_list = []
        for init_tile, end_tile in zip(init_chain_tiles, end_chain_tiles):
            enable_chains_trigger = self.trigger_manager.add_trigger(f'Bridge {bridge_number} enable chain', enabled=False)
            chain_trigger_list.append(enable_chains_trigger)
            i = 0
            init_chain_tile = Tile(init_tile.x, init_tile.y)

            while init_chain_tile != end_tile:
                if i % 2 == 0:
                    create_chain_trigger = self.trigger_manager.add_trigger(f'Bridge {bridge_number} chain {i}', enabled=False)
                    create_chain_trigger.new_condition.timer(timer=i + 2)
                    remove_tile = utils.increment_tile(init_chain_tile, increment, 1)
                    remove_area = Area.from_tiles(init_chain_tile, remove_tile)
                    for player in self.player_list:
                        create_chain_trigger.new_effect.kill_object(
                            source_player=player,
                            area_x1=remove_area.x1,
                            area_y1=remove_area.y1,
                            area_x2=remove_area.x2,
                            area_y2=remove_area.y2
                        )
                    create_chain_trigger.new_effect.create_object(
                        object_list_unit_id=intermediate_chain_unit,
                        source_player=PlayerId.GAIA,
                        location_x=init_chain_tile.x,
                        location_y=init_chain_tile.y
                    )
                    create_chain_trigger.new_effect.replace_object(
                        source_player=PlayerId.GAIA,
                        target_player=PlayerId.GAIA,
                        object_list_unit_id=intermediate_chain_unit,
                        object_list_unit_id_2=fixed_chain_unit,
                        area_x1=init_chain_tile.x,
                        area_y1=init_chain_tile.y,
                        area_x2=init_chain_tile.x,
                        area_y2=init_chain_tile.y
                    )
                    enable_chains_trigger.new_effect.activate_trigger(create_chain_trigger.trigger_id)
                init_chain_tile = utils.increment_tile(init_chain_tile, increment, 1)
                i += 1
            remove_area = Area.from_tiles(init_chain_tiles[0], end_chain_tiles[-1])
            remove_area.expand(1)
            remove_short_chain = self.trigger_manager.add_trigger(f'Bridge {bridge_number} remove short chain', enabled=False)
            enable_chains_trigger.new_effect.activate_trigger(remove_short_chain.trigger_id)
            remove_short_chain.new_condition.timer(timer=i + 2)
            remove_short_chain.new_effect.remove_object(
                source_player=PlayerId.GAIA,
                object_list_unit_id=short_chain_unit,
                area_x1=remove_area.x1,
                area_y1=remove_area.y1,
                area_x2=remove_area.x2,
                area_y2=remove_area.y2
            )
        return chain_trigger_list

    def retract_chain(self, bridge_number: int, init_chain_tiles: list[Tile], end_chain_tiles: list[Tile], increment: tuple[int, int],
                      init_shore_area: Area, end_shore_area: Area,
                      short_chain_unit: int, short_intermediate_chain_unit: int, fixed_chain_unit: int):
        chain_trigger_list = []
        short_chain_trigger = self.trigger_manager.add_trigger(f'Bridge {bridge_number} create short chain', enabled=False)
        for i, (init_tile, end_tile) in enumerate(zip(init_shore_area.to_coords(), end_shore_area.to_coords())):
            if i % 2 != 0:
                short_chain_trigger.new_effect.create_object(
                    object_list_unit_id=short_intermediate_chain_unit,
                    source_player=PlayerId.GAIA,
                    location_x=init_tile.x,
                    location_y=init_tile.y
                )
                short_chain_trigger.new_effect.create_object(
                    object_list_unit_id=short_intermediate_chain_unit,
                    source_player=PlayerId.GAIA,
                    location_x=end_tile.x,
                    location_y=end_tile.y
                )
                short_chain_trigger.new_effect.replace_object(
                    source_player=PlayerId.GAIA,
                    target_player=PlayerId.GAIA,
                    object_list_unit_id=short_intermediate_chain_unit,
                    object_list_unit_id_2=short_chain_unit,
                    area_x1=init_tile.x,
                    area_y1=init_tile.y,
                    area_x2=init_tile.x,
                    area_y2=init_tile.y
                )
                short_chain_trigger.new_effect.replace_object(
                    source_player=PlayerId.GAIA,
                    target_player=PlayerId.GAIA,
                    object_list_unit_id=short_intermediate_chain_unit,
                    object_list_unit_id_2=short_chain_unit,
                    area_x1=end_tile.x,
                    area_y1=end_tile.y,
                    area_x2=end_tile.x,
                    area_y2=end_tile.y
                )

        for init_tile, end_tile in zip(init_chain_tiles, end_chain_tiles):
            enable_chains_trigger = self.trigger_manager.add_trigger(f'Bridge {bridge_number} enable chain retract', enabled=False)
            chain_trigger_list.append(enable_chains_trigger)
            enable_chains_trigger.new_effect.activate_trigger(short_chain_trigger.trigger_id)
            i = 0
            init_chain_tile = Tile(init_tile.x, init_tile.y)
            while init_chain_tile != end_tile:
                if i % 2 == 0:
                    create_chain_trigger = self.trigger_manager.add_trigger(f'Bridge {bridge_number} retract chain {i}', enabled=False)
                    create_chain_trigger.new_condition.timer(timer=i + 2)
                    remove_tile = utils.increment_tile(init_chain_tile, increment, 1)
                    remove_area = Area.from_tiles(init_chain_tile, remove_tile)
                    for player in self.player_list:
                        create_chain_trigger.new_effect.kill_object(
                            source_player=player,
                            area_x1=remove_area.x1,
                            area_y1=remove_area.y1,
                            area_x2=remove_area.x2,
                            area_y2=remove_area.y2
                        )
                    create_chain_trigger.new_effect.remove_object(
                        object_list_unit_id=fixed_chain_unit,
                        source_player=PlayerId.GAIA,
                        area_x1=remove_area.x1,
                        area_y1=remove_area.y1,
                        area_x2=remove_area.x2,
                        area_y2=remove_area.y2
                    )
                    enable_chains_trigger.new_effect.activate_trigger(create_chain_trigger.trigger_id)
                init_chain_tile = utils.increment_tile(init_chain_tile, increment, 1)
                i += 1
        return chain_trigger_list

    def deploy_bridge(self, bridge_number: int,
                      moving_bridge_unit: int, bridge_piece: int, increment: tuple[int, int],
                      init_extreme_bridge_area: Area, end_extreme_bridge_area: Area,
                      init_deploy_bridge_area: Area, end_deploy_bridge_area: Area,
                      init_chain_tiles: list[Tile], end_chain_tiles: list[Tile],
                      short_chain_unit: int, intermediate_chain_unit: int, fixed_chain_unit: int):

        create_moving_bridge_trigger = self.trigger_manager.add_trigger(f'Bridge {bridge_number} deploy bridge', enabled=False)
        for player in self.player_list:
            create_moving_bridge_trigger.new_effect.play_sound(
                sound_name=self.bridge_sound,
                source_player=player,
                location_x=init_extreme_bridge_area.x1,
                location_y=init_extreme_bridge_area.y1
            )
        for tile in init_extreme_bridge_area.to_coords():
            create_moving_bridge_trigger.new_effect.create_object(
                object_list_unit_id=moving_bridge_unit,
                source_player=PlayerId.THREE,
                location_x=tile.x,
                location_y=tile.y
            )
            destination = utils.get_edge_tile(self.map_manager, tile, increment)
            create_moving_bridge_trigger.new_effect.task_object(
                object_list_unit_id=moving_bridge_unit,
                source_player=PlayerId.THREE,
                area_x1=tile.x,
                area_y1=tile.y,
                area_x2=tile.x,
                area_y2=tile.y,
                location_x=destination.x,
                location_y=destination.y,
                action_type=ActionType.MOVE
            )
        create_moving_bridge_trigger.new_effect.disable_unit_targeting(
            source_player=PlayerId.THREE,
            object_list_unit_id=moving_bridge_unit,
            area_x1=init_extreme_bridge_area.x1,
            area_y1=init_extreme_bridge_area.y1,
            area_x2=init_extreme_bridge_area.x2,
            area_y2=init_extreme_bridge_area.y2
        )
        create_moving_bridge_trigger.new_effect.change_object_stance(
            source_player=PlayerId.THREE,
            object_list_unit_id=moving_bridge_unit,
            area_x1=init_extreme_bridge_area.x1,
            area_y1=init_extreme_bridge_area.y1,
            area_x2=init_extreme_bridge_area.x2,
            area_y2=init_extreme_bridge_area.y2,
            attack_stance=AttackStance.NO_ATTACK_STANCE
        )
        remove_moving_trigger = self.trigger_manager.add_trigger(f'Bridge {bridge_number} remove deploy bridge', enabled=False)
        remove_moving_trigger.new_condition.objects_in_area(
            source_player=PlayerId.THREE,
            object_list=moving_bridge_unit,
            quantity=len(init_extreme_bridge_area.to_coords()),
            area_x1=end_extreme_bridge_area.x1,
            area_y1=end_extreme_bridge_area.y1,
            area_x2=end_extreme_bridge_area.x2,
            area_y2=end_extreme_bridge_area.y2
        )
        remove_moving_trigger.new_effect.remove_object(
            object_list_unit_id=moving_bridge_unit,
            source_player=PlayerId.THREE,
            area_x1=end_extreme_bridge_area.x1,
            area_y1=end_extreme_bridge_area.y1,
            area_x2=end_extreme_bridge_area.x2,
            area_y2=end_extreme_bridge_area.y2
        )
        step = 0
        moving_bridge_piece_triggers = []
        create_moving_bridge_trigger.new_effect.activate_trigger(remove_moving_trigger.trigger_id)
        while init_deploy_bridge_area.corner1 != end_deploy_bridge_area.corner1 or init_deploy_bridge_area.corner2 != end_deploy_bridge_area.corner2:
            create_bridge_piece_trigger = self.trigger_manager.add_trigger(f'Bridge {bridge_number} create bridge piece {step}', enabled=False)
            for tile in init_deploy_bridge_area.to_coords(as_terrain=True):
                create_bridge_piece_trigger.new_condition.objects_in_area(
                    source_player=PlayerId.THREE,
                    area_x1=tile.x,
                    area_y1=tile.y,
                    area_x2=tile.x,
                    area_y2=tile.y,
                    object_list=moving_bridge_unit,
                    quantity=1
                )
                for player in self.player_list:
                    create_bridge_piece_trigger.new_effect.kill_object(
                        source_player=player,
                        area_x1=tile.x,
                        area_y1=tile.y,
                        area_x2=tile.x,
                        area_y2=tile.y,
                    )
                create_bridge_piece_trigger.new_effect.create_object(
                    object_list_unit_id=bridge_piece,
                    source_player=PlayerId.THREE,
                    location_x=tile.x,
                    location_y=tile.y
                )
            moving_bridge_piece_triggers.append(create_bridge_piece_trigger)
            init_deploy_bridge_area.move(increment[0], increment[1])
            step += 1
        for trigger in moving_bridge_piece_triggers:
            create_moving_bridge_trigger.new_effect.activate_trigger(trigger_id=trigger.trigger_id)
        deploy_chain_trigger_list = self.deploy_chain(
            bridge_number=bridge_number,
            init_chain_tiles=init_chain_tiles,
            end_chain_tiles=end_chain_tiles,
            increment=increment,
            short_chain_unit=short_chain_unit,
            intermediate_chain_unit=intermediate_chain_unit,
            fixed_chain_unit=fixed_chain_unit
        )
        for chain_trigger in deploy_chain_trigger_list:
            create_moving_bridge_trigger.new_effect.activate_trigger(trigger_id=chain_trigger.trigger_id)
        return create_moving_bridge_trigger

    def retract_bridge(self, bridge_number: int,
                       moving_bridge_unit: int, bridge_piece: int, decrement: tuple[int, int],
                       init_extreme_bridge_area: Area, end_extreme_bridge_area: Area,
                       init_retract_bridge_area: Area, end_retract_bridge_area: Area,
                       init_shore_area: Area, end_shore_area: Area,
                       init_chain_tiles: list[Tile], end_chain_tiles: list[Tile],
                       short_chain_unit: int, short_intermediate_chain_unit: int, fixed_chain_unit: int):
        create_moving_bridge_trigger = self.trigger_manager.add_trigger(f'Bridge {bridge_number} create retract bridge', enabled=False)
        for player in self.player_list:
            create_moving_bridge_trigger.new_effect.play_sound(
                sound_name=self.bridge_sound,
                source_player=player,
                location_x=init_extreme_bridge_area.x1,
                location_y=init_extreme_bridge_area.y1
            )
        for tile in init_extreme_bridge_area.to_coords():
            create_moving_bridge_trigger.new_effect.create_object(
                object_list_unit_id=moving_bridge_unit,
                source_player=PlayerId.THREE,
                location_x=tile.x,
                location_y=tile.y
            )
            destination = utils.get_edge_tile(self.map_manager, tile, decrement)
            create_moving_bridge_trigger.new_effect.task_object(
                object_list_unit_id=moving_bridge_unit,
                source_player=PlayerId.THREE,
                area_x1=tile.x,
                area_y1=tile.y,
                area_x2=tile.x,
                area_y2=tile.y,
                location_x=destination.x,
                location_y=destination.y,
                action_type=ActionType.MOVE
            )
        create_moving_bridge_trigger.new_effect.disable_unit_targeting(
            source_player=PlayerId.THREE,
            object_list_unit_id=moving_bridge_unit,
            area_x1=init_extreme_bridge_area.x1,
            area_y1=init_extreme_bridge_area.y1,
            area_x2=init_extreme_bridge_area.x2,
            area_y2=init_extreme_bridge_area.y2
        )
        create_moving_bridge_trigger.new_effect.change_object_stance(
            source_player=PlayerId.THREE,
            object_list_unit_id=moving_bridge_unit,
            area_x1=init_extreme_bridge_area.x1,
            area_y1=init_extreme_bridge_area.y1,
            area_x2=init_extreme_bridge_area.x2,
            area_y2=init_extreme_bridge_area.y2,
            attack_stance=AttackStance.NO_ATTACK_STANCE
        )
        remove_moving_trigger = self.trigger_manager.add_trigger(f'Bridge {bridge_number} remove retract bridge', enabled=False)
        remove_moving_trigger.new_condition.objects_in_area(
            source_player=PlayerId.THREE,
            object_list=moving_bridge_unit,
            quantity=len(init_extreme_bridge_area.to_coords()),
            area_x1=end_extreme_bridge_area.x1,
            area_y1=end_extreme_bridge_area.y1,
            area_x2=end_extreme_bridge_area.x2,
            area_y2=end_extreme_bridge_area.y2
        )
        remove_moving_trigger.new_effect.remove_object(
            object_list_unit_id=moving_bridge_unit,
            source_player=PlayerId.THREE,
            area_x1=end_extreme_bridge_area.x1,
            area_y1=end_extreme_bridge_area.y1,
            area_x2=end_extreme_bridge_area.x2,
            area_y2=end_extreme_bridge_area.y2
        )
        step = 0
        moving_bridge_piece_triggers = []
        create_moving_bridge_trigger.new_effect.activate_trigger(remove_moving_trigger.trigger_id)
        while init_retract_bridge_area.corner1 != end_retract_bridge_area.corner1 or init_retract_bridge_area.corner2 != end_retract_bridge_area.corner2:
            create_bridge_piece_trigger = self.trigger_manager.add_trigger(f'Bridge {bridge_number} remove piece {step}', enabled=False)
            create_bridge_piece_trigger.new_condition.objects_in_area(
                source_player=PlayerId.THREE,
                area_x1=init_retract_bridge_area.x1,
                area_y1=init_retract_bridge_area.y1,
                area_x2=init_retract_bridge_area.x2,
                area_y2=init_retract_bridge_area.y2,
                object_list=moving_bridge_unit,
                quantity=1
            )
            for player in self.player_list:
                create_bridge_piece_trigger.new_effect.kill_object(
                    source_player=player,
                    area_x1=init_retract_bridge_area.x1,
                    area_y1=init_retract_bridge_area.y1,
                    area_x2=init_retract_bridge_area.x2,
                    area_y2=init_retract_bridge_area.y2,
                )
            create_bridge_piece_trigger.new_effect.remove_object(
                object_list_unit_id=bridge_piece,
                source_player=PlayerId.THREE,
                area_x1=init_retract_bridge_area.x1,
                area_y1=init_retract_bridge_area.y1,
                area_x2=init_retract_bridge_area.x2,
                area_y2=init_retract_bridge_area.y2
            )
            moving_bridge_piece_triggers.append(create_bridge_piece_trigger)
            init_retract_bridge_area.move(decrement[0], decrement[1])
            step += 1
        for trigger in moving_bridge_piece_triggers:
            create_moving_bridge_trigger.new_effect.activate_trigger(trigger_id=trigger.trigger_id)
        retract_chain_trigger_list = self.retract_chain(
            bridge_number=bridge_number,
            init_chain_tiles=init_chain_tiles,
            end_chain_tiles=end_chain_tiles,
            increment=decrement,
            init_shore_area=init_shore_area,
            end_shore_area=end_shore_area,
            short_chain_unit=short_chain_unit,
            short_intermediate_chain_unit=short_intermediate_chain_unit,
            fixed_chain_unit=fixed_chain_unit
        )
        for chain_trigger in retract_chain_trigger_list:
            create_moving_bridge_trigger.new_effect.activate_trigger(trigger_id=chain_trigger.trigger_id)
        return create_moving_bridge_trigger

    def generate_retractable_bridges(self, bridge_areas: list[Area], center_tile: Tile) -> list[tuple[Trigger, Trigger]]:
        bridge_triggers = []
        for i, area in enumerate(bridge_areas):
            extremes_bridge_area = area.copy()
            empty_bridge_area = area.copy()

            init_shore_area: Area = self.scenario.new.area()
            end_shore_area: Area = self.scenario.new.area()

            init_extreme_bridge_area = self.scenario.new.area()
            end_extreme_bridge_area = self.scenario.new.area()

            init_deploy_bridge_area = self.scenario.new.area()
            end_deploy_bridge_area = self.scenario.new.area()

            init_retract_bridge_area = self.scenario.new.area()
            end_retract_bridge_area = self.scenario.new.area()

            init_deploy_chain_tiles = []
            end_deploy_chain_tiles = []

            init_retract_chain_tiles = []
            end_retract_chain_tiles = []
            if area.get_width() > area.get_height():
                # VERTICAL
                extremes_bridge_area.shrink_x1(1)
                extremes_bridge_area.shrink_x2(1)
                empty_bridge_area.shrink_x1(2)
                empty_bridge_area.shrink_x2(2)
                moving_bridge_unit = self.VERTICAL_BRIDGE_UNIT
                bridge_piece = BuildingInfo.WOODEN_BRIDGE_A_MIDDLE.ID
                init_shore_area = utils.set_area_coordinates(init_shore_area, area.x1, area.x1, area.y1 - 1, area.y2 + 1)
                end_shore_area = utils.set_area_coordinates(end_shore_area, area.x2, area.x2, area.y1 - 1, area.y2 + 1)
                if extremes_bridge_area.x1 < center_tile.x:
                    # BRIDGE DEPLOYS TOWARDS THE SOUTH, RETRACTS TOWARDS THE NORTH
                    init_extreme_bridge_area = utils.set_area_coordinates(init_extreme_bridge_area, extremes_bridge_area.x2, extremes_bridge_area.x2, extremes_bridge_area.y1, extremes_bridge_area.y2)
                    end_extreme_bridge_area = utils.set_area_coordinates(end_extreme_bridge_area, extremes_bridge_area.x1, extremes_bridge_area.x1, extremes_bridge_area.y1, extremes_bridge_area.y2)
                    init_deploy_bridge_area = utils.set_area_coordinates(init_deploy_bridge_area, empty_bridge_area.x2, empty_bridge_area.x2, empty_bridge_area.y1, empty_bridge_area.y2)
                    end_deploy_bridge_area = utils.set_area_coordinates(end_deploy_bridge_area, extremes_bridge_area.x1, extremes_bridge_area.x1, extremes_bridge_area.y1, extremes_bridge_area.y2)
                    init_retract_bridge_area = utils.set_area_coordinates(init_retract_bridge_area, empty_bridge_area.x1, empty_bridge_area.x1, empty_bridge_area.y1, empty_bridge_area.y2)
                    end_retract_bridge_area = utils.set_area_coordinates(end_retract_bridge_area, extremes_bridge_area.x2, extremes_bridge_area.x2, extremes_bridge_area.y1, extremes_bridge_area.y2)
                    init_deploy_chain_tiles.append(Tile(end_shore_area.x1, end_shore_area.y1))
                    init_deploy_chain_tiles.append(Tile(end_shore_area.x1, end_shore_area.y2))
                    end_deploy_chain_tiles.append(Tile(init_shore_area.x2 - 1, init_shore_area.y1))
                    end_deploy_chain_tiles.append(Tile(init_shore_area.x2 - 1, init_shore_area.y2))
                    init_retract_chain_tiles.append(Tile(init_shore_area.x2, init_shore_area.y1))
                    init_retract_chain_tiles.append(Tile(init_shore_area.x2, init_shore_area.y2))
                    end_retract_chain_tiles.append(Tile(end_shore_area.x1, end_shore_area.y1))
                    end_retract_chain_tiles.append(Tile(end_shore_area.x1, end_shore_area.y2))
                    short_chain_unit = self.HORIZONTAL_CHAIN_FIXED_UNIT
                    short_intermediate_chain_unit = self.HORIZONTAL_CHAIN_INTERMEDIATE_UNIT
                    intermediate_chain_unit = self.VERTICAL_CHAIN_INTERMEDIATE_UNIT
                    fixed_chain_unit = self.VERTICAL_CHAIN_FIXED_UNIT
                    init_bridge_unit = BuildingInfo.WOODEN_BRIDGE_A_TOP.ID
                    end_bridge_unit = BuildingInfo.WOODEN_BRIDGE_A_BOTTOM.ID
                    increment = (-1, 0)
                    decrement = (1, 0)
                else:
                    # BRIDGE DEPLOYS TOWARDS THE NORTH, RETRACTS TOWARDS THE SOUTH
                    init_extreme_bridge_area = utils.set_area_coordinates(init_extreme_bridge_area, extremes_bridge_area.x1, extremes_bridge_area.x1, extremes_bridge_area.y1, extremes_bridge_area.y2)
                    end_extreme_bridge_area = utils.set_area_coordinates(end_extreme_bridge_area, extremes_bridge_area.x2, extremes_bridge_area.x2, extremes_bridge_area.y1, extremes_bridge_area.y2)
                    init_deploy_bridge_area = utils.set_area_coordinates(init_deploy_bridge_area, empty_bridge_area.x1, empty_bridge_area.x1, empty_bridge_area.y1, empty_bridge_area.y2)
                    end_deploy_bridge_area = utils.set_area_coordinates(end_deploy_bridge_area, extremes_bridge_area.x2, extremes_bridge_area.x2, extremes_bridge_area.y1, extremes_bridge_area.y2)
                    init_retract_bridge_area = utils.set_area_coordinates(init_deploy_bridge_area, empty_bridge_area.x2, empty_bridge_area.x2, empty_bridge_area.y1, empty_bridge_area.y2)
                    end_retract_bridge_area = utils.set_area_coordinates(end_deploy_bridge_area, extremes_bridge_area.x1, extremes_bridge_area.x1, extremes_bridge_area.y1, extremes_bridge_area.y2)
                    init_deploy_chain_tiles.append(Tile(init_shore_area.x2 - 1,  init_shore_area.y1))
                    init_deploy_chain_tiles.append(Tile(init_shore_area.x2 - 1, init_shore_area.y2))
                    end_deploy_chain_tiles.append(Tile(end_shore_area.x1 + 1, end_shore_area.y1))
                    end_deploy_chain_tiles.append(Tile(end_shore_area.x1 + 1, end_shore_area.y2))
                    end_retract_chain_tiles.append(Tile(init_shore_area.x2, init_shore_area.y1))
                    end_retract_chain_tiles.append(Tile(init_shore_area.x2, init_shore_area.y2))
                    init_retract_chain_tiles.append(Tile(end_shore_area.x1, end_shore_area.y1))
                    init_retract_chain_tiles.append(Tile(end_shore_area.x1, end_shore_area.y2))
                    short_chain_unit = self.HORIZONTAL_CHAIN_FIXED_UNIT
                    short_intermediate_chain_unit = self.HORIZONTAL_CHAIN_INTERMEDIATE_UNIT
                    intermediate_chain_unit = self.VERTICAL_CHAIN_INTERMEDIATE_UNIT
                    fixed_chain_unit = self.VERTICAL_CHAIN_FIXED_UNIT
                    init_bridge_unit = BuildingInfo.WOODEN_BRIDGE_A_BOTTOM.ID
                    end_bridge_unit = BuildingInfo.WOODEN_BRIDGE_A_TOP.ID
                    increment = (1, 0)
                    decrement = (-1, 0)
            else:
                # HORIZONTAL
                extremes_bridge_area.shrink_y1(1)
                extremes_bridge_area.shrink_y2(1)
                empty_bridge_area.shrink_y1(2)
                empty_bridge_area.shrink_y2(2)
                moving_bridge_unit = self.HORIZONTAL_BRIDGE_UNIT
                bridge_piece = BuildingInfo.WOODEN_BRIDGE_B_MIDDLE.ID
                init_shore_area = utils.set_area_coordinates(init_shore_area, area.x1 - 1, area.x2 + 1, area.y1, area.y1)
                end_shore_area = utils.set_area_coordinates(end_shore_area, area.x1 - 1, area.x2 + 1, area.y2, area.y2)
                if extremes_bridge_area.y1 < center_tile.y:
                    # BRIDGE DEPLOYS TOWARDS THE LEFT, RETRACTS TOWARDS THE RIGHT
                    init_extreme_bridge_area = utils.set_area_coordinates(init_extreme_bridge_area, extremes_bridge_area.x1, extremes_bridge_area.x2, extremes_bridge_area.y2, extremes_bridge_area.y2)
                    end_extreme_bridge_area = utils.set_area_coordinates(end_extreme_bridge_area, extremes_bridge_area.x1, extremes_bridge_area.x2, extremes_bridge_area.y1, extremes_bridge_area.y1)
                    init_deploy_bridge_area = utils.set_area_coordinates(init_deploy_bridge_area, empty_bridge_area.x1, empty_bridge_area.x2, empty_bridge_area.y2, empty_bridge_area.y2)
                    end_deploy_bridge_area = utils.set_area_coordinates(end_deploy_bridge_area, extremes_bridge_area.x1, extremes_bridge_area.x2, extremes_bridge_area.y1, extremes_bridge_area.y1)
                    init_retract_bridge_area = utils.set_area_coordinates(init_retract_bridge_area, empty_bridge_area.x1, empty_bridge_area.x2, empty_bridge_area.y1, empty_bridge_area.y1)
                    end_retract_bridge_area = utils.set_area_coordinates(end_retract_bridge_area, extremes_bridge_area.x1, extremes_bridge_area.x2, extremes_bridge_area.y2, extremes_bridge_area.y2)
                    init_deploy_chain_tiles.append(Tile(end_shore_area.x1, end_shore_area.y1))
                    init_deploy_chain_tiles.append(Tile(end_shore_area.x2, end_shore_area.y1))
                    end_deploy_chain_tiles.append(Tile(init_shore_area.x1, init_shore_area.y2 - 1))
                    end_deploy_chain_tiles.append(Tile(init_shore_area.x2, init_shore_area.y2 - 1))
                    init_retract_chain_tiles.append(Tile(init_shore_area.x1, init_shore_area.y2))
                    init_retract_chain_tiles.append(Tile(init_shore_area.x2, init_shore_area.y2))
                    end_retract_chain_tiles.append(Tile(end_shore_area.x1, end_shore_area.y1))
                    end_retract_chain_tiles.append(Tile(end_shore_area.x2, end_shore_area.y1))
                    short_chain_unit = self.VERTICAL_CHAIN_FIXED_UNIT
                    short_intermediate_chain_unit = self.VERTICAL_CHAIN_INTERMEDIATE_UNIT
                    intermediate_chain_unit = self.HORIZONTAL_CHAIN_INTERMEDIATE_UNIT
                    fixed_chain_unit = self.HORIZONTAL_CHAIN_FIXED_UNIT
                    init_bridge_unit = BuildingInfo.WOODEN_BRIDGE_B_BOTTOM.ID
                    end_bridge_unit = BuildingInfo.WOODEN_BRIDGE_B_TOP.ID
                    increment = (0, -1)
                    decrement = (0, 1)
                else:
                    # BRIDGE DEPLOYS TOWARDS THE RIGHT, RETRACTS TOWARDS THE LEFT
                    init_extreme_bridge_area = utils.set_area_coordinates(init_extreme_bridge_area, extremes_bridge_area.x1, extremes_bridge_area.x2, extremes_bridge_area.y1, extremes_bridge_area.y1)
                    end_extreme_bridge_area = utils.set_area_coordinates(end_extreme_bridge_area, extremes_bridge_area.x1, extremes_bridge_area.x2, extremes_bridge_area.y2, extremes_bridge_area.y2)
                    init_deploy_bridge_area = utils.set_area_coordinates(init_deploy_bridge_area, empty_bridge_area.x1, empty_bridge_area.x2, empty_bridge_area.y1, empty_bridge_area.y1)
                    end_deploy_bridge_area = utils.set_area_coordinates(end_deploy_bridge_area, extremes_bridge_area.x1, extremes_bridge_area.x2, extremes_bridge_area.y2, extremes_bridge_area.y2)
                    init_retract_bridge_area = utils.set_area_coordinates(init_retract_bridge_area, empty_bridge_area.x1, empty_bridge_area.x2, empty_bridge_area.y2, empty_bridge_area.y2)
                    end_retract_bridge_area = utils.set_area_coordinates(end_retract_bridge_area, extremes_bridge_area.x1, extremes_bridge_area.x2, extremes_bridge_area.y1, extremes_bridge_area.y1)
                    init_deploy_chain_tiles.append(Tile(init_shore_area.x1, init_shore_area.y2 + 1))
                    init_deploy_chain_tiles.append(Tile(init_shore_area.x2, init_shore_area.y2 + 1))
                    end_deploy_chain_tiles.append(Tile(end_shore_area.x1, end_shore_area.y1 + 1))
                    end_deploy_chain_tiles.append(Tile(end_shore_area.x2, end_shore_area.y1 + 1))
                    init_retract_chain_tiles.append(Tile(end_shore_area.x1, end_shore_area.y1))
                    init_retract_chain_tiles.append(Tile(end_shore_area.x2, end_shore_area.y1))
                    end_retract_chain_tiles.append(Tile(init_shore_area.x1, init_shore_area.y2))
                    end_retract_chain_tiles.append(Tile(init_shore_area.x2, init_shore_area.y2))
                    short_chain_unit = self.VERTICAL_CHAIN_FIXED_UNIT
                    short_intermediate_chain_unit = self.VERTICAL_CHAIN_INTERMEDIATE_UNIT
                    intermediate_chain_unit = self.HORIZONTAL_CHAIN_INTERMEDIATE_UNIT
                    fixed_chain_unit = self.HORIZONTAL_CHAIN_FIXED_UNIT
                    init_bridge_unit = BuildingInfo.WOODEN_BRIDGE_B_TOP.ID
                    end_bridge_unit = BuildingInfo.WOODEN_BRIDGE_B_BOTTOM.ID
                    increment = (0, 1)
                    decrement = (0, -1)

            self.initial_bridges(i, init_bridge_unit, end_bridge_unit, short_chain_unit, extremes_bridge_area, init_extreme_bridge_area, end_extreme_bridge_area, init_shore_area, end_shore_area)

            deploy_bridge_trigger = self.deploy_bridge(
                bridge_number=i,
                moving_bridge_unit=moving_bridge_unit,
                bridge_piece=bridge_piece,
                increment=increment,
                init_extreme_bridge_area=init_extreme_bridge_area,
                end_extreme_bridge_area=end_extreme_bridge_area,
                init_deploy_bridge_area=init_deploy_bridge_area,
                end_deploy_bridge_area=end_deploy_bridge_area,
                init_chain_tiles=init_deploy_chain_tiles,
                end_chain_tiles=end_deploy_chain_tiles,
                short_chain_unit=short_chain_unit,
                intermediate_chain_unit=intermediate_chain_unit,
                fixed_chain_unit=fixed_chain_unit
            )
            retract_bridge_trigger = self.retract_bridge(
                bridge_number=i,
                moving_bridge_unit=moving_bridge_unit,
                bridge_piece=bridge_piece,
                decrement=decrement,
                init_extreme_bridge_area=end_extreme_bridge_area,
                end_extreme_bridge_area=init_extreme_bridge_area,
                init_retract_bridge_area=init_retract_bridge_area,
                end_retract_bridge_area=end_retract_bridge_area,
                init_shore_area=init_shore_area,
                end_shore_area=end_shore_area,
                init_chain_tiles=init_retract_chain_tiles,
                end_chain_tiles=end_retract_chain_tiles,
                short_chain_unit=short_chain_unit,
                short_intermediate_chain_unit=short_intermediate_chain_unit,
                fixed_chain_unit=fixed_chain_unit
            )
            bridge_triggers.append((deploy_bridge_trigger, retract_bridge_trigger))
        return bridge_triggers

    def set_bridge_stats(self):
        module_dir = Path(__file__).parent
        xs_file = module_dir / "xs/bridge_stats.xs"
        self.xs_manager.add_script(xs_file_path=str(xs_file))
        xs_trigger = self.trigger_manager.add_trigger("XS CALL BRIDGE_STATS")
        xs_trigger.new_effect.script_call(message="bridge_stats();")
