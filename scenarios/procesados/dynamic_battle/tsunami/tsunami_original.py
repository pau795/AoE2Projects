import math

from AoE2ScenarioParser.datasets.other import OtherInfo
from AoE2ScenarioParser.datasets.players import PlayerId
from AoE2ScenarioParser.datasets.trigger_lists import ObjectAttribute, Operation, ActionType, TerrainRestrictions, ObjectClass
from AoE2ScenarioParser.datasets.units import UnitInfo
from scenarios.lib.parser_project import ParserProject


class Tsunami(ParserProject):

    def __init__(self, input_scenario_name:str, output_scenario_name:str):
        super().__init__(input_scenario_name, output_scenario_name)
        self.tsunami_period = 600
        self.tsunami_unit_damage = 50
        self.tsunami_building_damage = 300
        self.tsunami_sound = "sirena60"

        self.map_manager = self.scenario.map_manager
        self.trigger_manager = self.scenario.trigger_manager
        self.first_wave = self.trigger_manager.add_trigger("First wave", enabled=False)
        self.second_wave = self.trigger_manager.add_trigger("Second wave", enabled=False)
        self.third_wave = self.trigger_manager.add_trigger("Third wave", enabled=False)

    def wave(self, x):
        x_interpol = 2 * math.pi / ((self.scenario.map_manager.map_width - 1.0) / 2.0) * (x % ((self.scenario.map_manager.map_width - 1.0) / 2.0))
        return (math.sin(x_interpol) + 1) * 5

    @staticmethod
    def wave_time(y):
        return int(y / 2 + 1)

    def new_round(self, i, timer, enable_damage_trigger):
        wave_round = self.scenario.trigger_manager.add_trigger(f'Wave Round {i}')
        wave_round.new_condition.timer(
            timer=timer
        )
        wave_round.new_effect.activate_trigger(
            trigger_id=enable_damage_trigger.trigger_id
        )
        wave_round.new_effect.activate_trigger(
            trigger_id=self.first_wave.trigger_id
        )
        wave_round.new_effect.activate_trigger(
            trigger_id=self.second_wave.trigger_id
        )
        wave_round.new_effect.activate_trigger(
            trigger_id=self.third_wave.trigger_id
        )

    def process(self):
        wave_cords = self.map_manager.get_square_1d(x1=0, y1=0, x2=self.map_manager.map_width - 1, y2=10)
        sin_x = [self.wave(x) for x in range(0, self.map_manager.map_width)]

        initial_stats = self.trigger_manager.add_trigger("Initial Stats")
        initial_stats.new_effect.modify_attribute(
            object_list_unit_id=UnitInfo.SNOW_LEOPARD.ID,
            source_player=PlayerId.GAIA,
            object_attributes=ObjectAttribute.STANDING_GRAPHIC,
            operation=Operation.SET,
            quantity=7569
        )

        initial_stats.new_effect.modify_attribute(
            object_list_unit_id=UnitInfo.SNOW_LEOPARD.ID,
            source_player=PlayerId.GAIA,
            object_attributes=ObjectAttribute.WALKING_GRAPHIC,
            operation=Operation.SET,
            quantity=7569
        )

        initial_stats.new_effect.modify_attribute(
            object_list_unit_id=UnitInfo.SNOW_LEOPARD.ID,
            source_player=PlayerId.GAIA,
            object_attributes=ObjectAttribute.DYING_GRAPHIC,
            operation=Operation.SET,
            quantity=5507
        )

        initial_stats.new_effect.modify_attribute(
            object_list_unit_id=UnitInfo.SNOW_LEOPARD.ID,
            source_player=PlayerId.GAIA,
            object_attributes=ObjectAttribute.DEAD_UNIT_ID,
            operation=Operation.SET,
            quantity=2
        )
        initial_stats.new_effect.modify_attribute(
            object_list_unit_id=UnitInfo.SNOW_LEOPARD.ID,
            source_player=PlayerId.GAIA,
            object_attributes=ObjectAttribute.DEAD_UNIT_ID,
            operation=Operation.DIVIDE,
            quantity=-2
        )

        initial_stats.new_effect.modify_attribute(
            object_list_unit_id=UnitInfo.SNOW_LEOPARD.ID,
            source_player=PlayerId.GAIA,
            object_attributes=ObjectAttribute.TERRAIN_RESTRICTION_ID,
            operation=Operation.SET,
            quantity=TerrainRestrictions.ALL
        )

        initial_stats.new_effect.modify_attribute(
            object_list_unit_id=UnitInfo.SNOW_LEOPARD.ID,
            source_player=PlayerId.GAIA,
            object_attributes=ObjectAttribute.UNIT_SIZE_X,
            operation=Operation.SET,
            quantity=0
        )

        initial_stats.new_effect.modify_attribute(
            object_list_unit_id=UnitInfo.SNOW_LEOPARD.ID,
            source_player=PlayerId.GAIA,
            object_attributes=ObjectAttribute.UNIT_SIZE_Y,
            operation=Operation.SET,
            quantity=0
        )

        initial_stats.new_effect.modify_attribute(
            object_list_unit_id=UnitInfo.SNOW_LEOPARD.ID,
            source_player=PlayerId.GAIA,
            object_attributes=ObjectAttribute.UNIT_SIZE_Z,
            operation=Operation.SET,
            quantity=0
        )

        initial_stats.new_effect.modify_attribute(
            object_list_unit_id=UnitInfo.SNOW_LEOPARD.ID,
            source_player=PlayerId.GAIA,
            object_attributes=ObjectAttribute.MOVEMENT_SPEED,
            operation=Operation.SET,
            quantity=2
        )

        initial_stats.new_effect.modify_attribute(
            object_list_unit_id=OtherInfo.TREE_BIRCH.ID,
            source_player=PlayerId.GAIA,
            object_attributes=ObjectAttribute.AMOUNT_OF_1ST_RESOURCE_STORAGE,
            operation=Operation.SET,
            quantity=250
        )

        initial_stats.new_effect.modify_attribute(
            object_list_unit_id=OtherInfo.TREE_PALM_FOREST.ID,
            source_player=PlayerId.GAIA,
            object_attributes=ObjectAttribute.AMOUNT_OF_1ST_RESOURCE_STORAGE,
            operation=Operation.SET,
            quantity=250
        )

        replace_trees = self.trigger_manager.add_trigger("Replace Trees")
        replace_trees.new_effect.replace_object(
            object_list_unit_id=OtherInfo.TREE_BIRCH.ID,
            source_player=PlayerId.GAIA,
            target_player=PlayerId.GAIA,
            object_list_unit_id_2=OtherInfo.FLAG_A.ID
        )

        replace_trees.new_effect.replace_object(
            object_list_unit_id=OtherInfo.FLAG_A.ID,
            source_player=PlayerId.GAIA,
            target_player=PlayerId.GAIA,
            object_list_unit_id_2=OtherInfo.TREE_BIRCH.ID
        )

        replace_trees.new_effect.replace_object(
            object_list_unit_id=OtherInfo.TREE_PALM_FOREST.ID,
            source_player=PlayerId.GAIA,
            target_player=PlayerId.GAIA,
            object_list_unit_id_2=OtherInfo.FLAG_B.ID
        )

        replace_trees.new_effect.replace_object(
            object_list_unit_id=OtherInfo.FLAG_B.ID,
            source_player=PlayerId.GAIA,
            target_player=PlayerId.GAIA,
            object_list_unit_id_2=OtherInfo.TREE_PALM_FOREST.ID
        )

        create_wave = self.trigger_manager.add_trigger("Create Wave", enabled=False)
        for x in wave_cords:
            x_sin = sin_x[x.x]
            if x_sin - 1.5 < x.y < x_sin + 1.5:
                create_wave.new_effect.create_object(
                    object_list_unit_id=UnitInfo.SNOW_LEOPARD.ID,
                    location_x=x.x,
                    location_y=x.y,
                    source_player=PlayerId.GAIA
                )
                create_wave.new_effect.task_object(
                    object_list_unit_id=UnitInfo.SNOW_LEOPARD.ID,
                    location_x=x.x,
                    location_y=self.map_manager.map_height - 1,
                    area_x1=x.x,
                    area_x2=x.x,
                    area_y1=x.y,
                    area_y2=x.y,
                    source_player=PlayerId.GAIA,
                    action_type=ActionType.MOVE
                )
                for height in range(x.y, self.map_manager.map_height - 1):
                    tile = self.map_manager.get_tile(x.x, height)
                    if tile.elevation > 0:
                        remove_wave = self.trigger_manager.add_trigger("Remove Wave", looping=True)
                        remove_wave.new_condition.objects_in_area(
                            object_list=UnitInfo.SNOW_LEOPARD.ID,
                            source_player=PlayerId.GAIA,
                            area_x1=tile.x,
                            area_y1=tile.y,
                            area_x2=tile.x,
                            area_y2=tile.y + 3,
                            quantity=1
                        )
                        remove_wave.new_effect.kill_object(
                            object_list_unit_id=UnitInfo.SNOW_LEOPARD.ID,
                            area_x1=tile.x,
                            area_y1=tile.y,
                            area_x2=tile.x,
                            area_y2=tile.y + 3,
                            source_player=PlayerId.GAIA
                        )
                        break

        remove_waves_end = self.trigger_manager.add_trigger("Remove Waves End", looping=True)
        remove_waves_end.new_effect.kill_object(
            object_list_unit_id=UnitInfo.SNOW_LEOPARD.ID,
            area_x1=0,
            area_y1=self.map_manager.map_height - 1,
            area_x2=self.map_manager.map_width - 1,
            area_y2=self.map_manager.map_height - 1,
            source_player=PlayerId.GAIA
        )
        enable_wave_damage = self.trigger_manager.add_trigger("Enable Wave Damage", enabled=False)

        self.first_wave.new_effect.activate_trigger(
            trigger_id=create_wave.trigger_id
        )
        self.first_wave.new_effect.play_sound(
            sound_name=self.tsunami_sound,
            source_player=PlayerId.ONE
        )
        self.first_wave.new_effect.play_sound(
            sound_name=self.tsunami_sound,
            source_player=PlayerId.TWO
        )
        self.second_wave.new_condition.timer(
            timer=15,
        )
        self.second_wave.new_effect.activate_trigger(
            trigger_id=create_wave.trigger_id
        )

        self.third_wave.new_condition.timer(
            timer=30,
        )
        self.third_wave.new_effect.activate_trigger(
            trigger_id=create_wave.trigger_id
        )

        for x in range(1, 20):
            self.new_round(x, x * self.tsunami_period, enable_wave_damage)

        for w in [0, 15, 30]:
            invalidate_x = []
            for y in range(0, self.map_manager.map_height - 10):
                wave_cords1 = self.map_manager.get_square_1d(x1=0, y1=y, x2=self.map_manager.map_width - 1, y2=y + 10)
                wave_damage = self.trigger_manager.add_trigger("Wave Damage", enabled=False)
                enable_wave_damage.new_effect.activate_trigger(
                    trigger_id=wave_damage.trigger_id
                )
                wave_damage.new_condition.timer(
                    timer=self.wave_time(y) + w
                )
                for tile in wave_cords1:
                    if tile.x not in invalidate_x:
                        x_sin = sin_x[tile.x] + y
                        if x_sin - 0.75 < tile.y < x_sin + 0.75:
                            if tile.elevation > 0:
                                invalidate_x.append(tile.x)
                            for player in [PlayerId.ONE, PlayerId.TWO]:
                                wave_damage.new_effect.damage_object(
                                    area_x1=tile.x,
                                    area_y1=tile.y-2,
                                    area_x2=tile.x,
                                    area_y2=tile.y-2,
                                    source_player=player,
                                    quantity=self.tsunami_unit_damage
                                )
                                wave_damage.new_effect.damage_object(
                                    area_x1=tile.x,
                                    area_y1=tile.y-2,
                                    area_x2=tile.x,
                                    area_y2=tile.y-2,
                                    source_player=player,
                                    object_group=ObjectClass.BUILDING,
                                    quantity=self.tsunami_building_damage
                                )
                                wave_damage.new_effect.damage_object(
                                    area_x1=tile.x,
                                    area_y1=tile.y - 2,
                                    area_x2=tile.x,
                                    area_y2=tile.y - 2,
                                    source_player=player,
                                    object_group=ObjectClass.TOWER,
                                    quantity=self.tsunami_building_damage
                                )
                                wave_damage.new_effect.damage_object(
                                    area_x1=tile.x,
                                    area_y1=tile.y - 2,
                                    area_x2=tile.x,
                                    area_y2=tile.y - 2,
                                    source_player=player,
                                    object_group=ObjectClass.WALL,
                                    quantity=self.tsunami_building_damage
                                )


tsunami = Tsunami(
    input_scenario_name="TSUNAMI",
    output_scenario_name="tsunami_output"
)
tsunami.convert()
