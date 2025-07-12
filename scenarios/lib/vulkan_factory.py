from AoE2ScenarioParser.datasets.buildings import BuildingInfo
from AoE2ScenarioParser.datasets.other import OtherInfo
from AoE2ScenarioParser.datasets.players import PlayerId
from AoE2ScenarioParser.datasets.terrains import TerrainId
from AoE2ScenarioParser.datasets.trigger_lists import ObjectAttribute, Operation, PanelLocation
from AoE2ScenarioParser.datasets.units import UnitInfo

from scenarios.lib.area_optimizer import AreaOptimizer


class VulkanFactory:

    def __init__(self,
                 scenario,
                 first_stage_time=600,
                 second_stage_time=1200,
                 explosion_period=130,
                 lava_damage=30,
                 volcan_sound='volcan',
                 player_list=None):
        self.scenario = scenario
        self.first_stage_time = first_stage_time
        self.second_stage_time = second_stage_time
        self.explosion_period = explosion_period
        self.lava_damage = lava_damage
        self.volcan_sound = volcan_sound
        self.player_list = player_list
        self.generate_vulkan()

    def generate_vulkan(self):

        trigger_manager = self.scenario.trigger_manager
        unit_manager = self.scenario.unit_manager

        area = self.scenario.new.area().select_entire_map()

        initial_stats = trigger_manager.add_trigger("Initial Stats", enabled=True, looping=False)
        initial_stats.new_effect.modify_attribute(
            source_player=PlayerId.GAIA,
            object_list_unit_id=UnitInfo.HAWK.ID,
            object_attributes=ObjectAttribute.HIT_POINTS,
            operation=Operation.SET,
            quantity=0
        )
        initial_stats.new_effect.modify_attribute(
            source_player=PlayerId.GAIA,
            object_list_unit_id=UnitInfo.FALCON.ID,
            object_attributes=ObjectAttribute.HIT_POINTS,
            operation=Operation.SET,
            quantity=0
        )
        initial_stats.new_effect.modify_attribute(
            source_player=PlayerId.GAIA,
            object_list_unit_id=BuildingInfo.WOODEN_BRIDGE_A_TOP.ID,
            object_attributes=ObjectAttribute.FOUNDATION_TERRAIN,
            operation=Operation.SET,
            quantity=TerrainId.BLACK
        )

        road_aux_units = trigger_manager.add_trigger("Road Auxiliary Units", enabled=False, looping=False)
        farm_aux_units = trigger_manager.add_trigger("Farm Auxiliary Units", enabled=False, looping=False)

        road_timer = trigger_manager.add_trigger("Road Timer", enabled=True, looping=False)
        farm_timer = trigger_manager.add_trigger("Farm Timer", enabled=True, looping=False)

        initial_lava_damage = trigger_manager.add_trigger("Damage Initial Lava Tiles", enabled=True, looping=True)
        road_lava_damage = trigger_manager.add_trigger("Damage Road Lava Tiles", enabled=False, looping=True)
        farm_lava_damage = trigger_manager.add_trigger("Damage Farm Lava Tiles", enabled=False, looping=True)
        initial_lava_tiles = []
        road_lava_tiles = []
        farm_lava_tiles = []

        road_timer.new_condition.timer(
            timer=self.first_stage_time
        )
        road_timer.new_effect.activate_trigger(
            trigger_id=road_aux_units.trigger_id
        )

        farm_timer.new_condition.timer(
            timer=self.second_stage_time
        )
        farm_timer.new_effect.activate_trigger(
            trigger_id=farm_aux_units.trigger_id
        )

        for tile in area.to_coords(as_terrain=True):
            if tile.terrain_id == TerrainId.BLACK:
                initial_lava_tiles.append(tile)
            if tile.terrain_id == TerrainId.ROAD:
                road_lava_tiles.append(tile)
                road_aux_units.new_effect.create_object(
                    source_player=PlayerId.GAIA,
                    object_list_unit_id=BuildingInfo.WOODEN_BRIDGE_A_TOP.ID,
                    location_x=tile.x,
                    location_y=tile.y,
                )
                road_aux_units.new_effect.create_object(
                    source_player=PlayerId.GAIA,
                    object_list_unit_id=UnitInfo.HAWK.ID,
                    location_x=tile.x,
                    location_y=tile.y,
                )
                tile.terrain_id = TerrainId.BEACH_WET_GRAVEL
            if tile.terrain_id == TerrainId.FARM or tile.terrain_id == TerrainId.WATER_GREEN:
                farm_lava_tiles.append(tile)
                farm_aux_units.new_effect.create_object(
                    source_player=PlayerId.GAIA,
                    object_list_unit_id=BuildingInfo.WOODEN_BRIDGE_A_TOP.ID,
                    location_x=tile.x,
                    location_y=tile.y,
                )
                farm_aux_units.new_effect.create_object(
                    source_player=PlayerId.GAIA,
                    object_list_unit_id=UnitInfo.HAWK.ID,
                    location_x=tile.x,
                    location_y=tile.y,
                )
                if tile.terrain_id == TerrainId.FARM:
                    tile.terrain_id = TerrainId.BEACH_WET_GRAVEL

        road_aux_units.new_effect.remove_object(
            source_player=PlayerId.GAIA,
            object_list_unit_id=BuildingInfo.WOODEN_BRIDGE_A_TOP.ID,
            area_x1=area.x1,
            area_y1=area.y1,
            area_x2=area.x2,
            area_y2=area.y2,
        )
        road_aux_units.new_effect.display_instructions(
            object_list_unit_id=OtherInfo.STONE_MINE.ID,
            source_player=PlayerId.GAIA,
            sound_name=self.volcan_sound,
            message="The lava is rising!",
            display_time=20,
            instruction_panel_position=PanelLocation.TOP
        )

        farm_aux_units.new_effect.remove_object(
            source_player=PlayerId.GAIA,
            object_list_unit_id=BuildingInfo.WOODEN_BRIDGE_A_TOP.ID,
            area_x1=area.x1,
            area_y1=area.y1,
            area_x2=area.x2,
            area_y2=area.y2,
        )
        farm_aux_units.new_effect.display_instructions(
            object_list_unit_id=OtherInfo.STONE_MINE.ID,
            source_player=PlayerId.GAIA,
            sound_name=self.volcan_sound,
            display_time=20,
            instruction_panel_position=PanelLocation.TOP
        )

        road_aux_units.new_effect.activate_trigger(
            trigger_id=road_lava_damage.trigger_id
        )
        farm_aux_units.new_effect.activate_trigger(
            trigger_id=farm_lava_damage.trigger_id
        )
        area_optimizer = AreaOptimizer(self.scenario)
        initial_lava_areas = area_optimizer.optimize_area(tile_list=initial_lava_tiles)
        print(f'Initial lava tiles: {len(initial_lava_tiles)}, areas: {len(initial_lava_areas)}')
        road_lava_areas = area_optimizer.optimize_area(tile_list=road_lava_tiles)
        print(f'Road lava tiles: {len(road_lava_tiles)}, areas: {len(road_lava_areas)}')
        farm_lava_areas = area_optimizer.optimize_area(tile_list=farm_lava_tiles)
        print(f'Farm lava tiles: {len(farm_lava_tiles)}, areas: {len(farm_lava_areas)}')

        for initial_lava_area in initial_lava_areas:
            for player in self.player_list:
                initial_lava_damage.new_effect.damage_object(
                    source_player=player,
                    area_x1=initial_lava_area.x1,
                    area_y1=initial_lava_area.y1,
                    area_x2=initial_lava_area.x2,
                    area_y2=initial_lava_area.y2,
                    quantity=self.lava_damage
                )

        for road_lava_area in road_lava_areas:
            for player in self.player_list:
                road_lava_damage.new_effect.damage_object(
                    source_player=player,
                    area_x1=road_lava_area.x1,
                    area_y1=road_lava_area.y1,
                    area_x2=road_lava_area.x2,
                    area_y2=road_lava_area.y2,
                    quantity=self.lava_damage
                )

        for farm_lava_area in farm_lava_areas:
            for player in self.player_list:
                farm_lava_damage.new_effect.damage_object(
                    source_player=player,
                    area_x1=farm_lava_area.x1,
                    area_y1=farm_lava_area.y1,
                    area_x2=farm_lava_area.x2,
                    area_y2=farm_lava_area.y2,
                    quantity=self.lava_damage
                )

        periodic_explosions = trigger_manager.add_trigger('Periodic Explosions', enabled=True, looping=True)
        periodic_explosions.new_condition.timer(
            timer=self.explosion_period
        )
        units = unit_manager.get_units_in_area(x1=area.x1, y1=area.y1, x2=area.x2, y2=area.y2)
        for unit in units:
            if unit.unit_const == UnitInfo.HAWK.ID or unit.unit_const == UnitInfo.FALCON.ID:
                periodic_explosions.new_effect.create_object(
                    source_player=PlayerId.GAIA,
                    object_list_unit_id=UnitInfo.HAWK.ID,
                    location_x=int(unit.x),
                    location_y=int(unit.y)
                )
