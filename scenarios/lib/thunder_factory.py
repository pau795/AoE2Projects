import math
import random

from AoE2ScenarioParser.datasets.other import OtherInfo
from AoE2ScenarioParser.datasets.players import PlayerId
from AoE2ScenarioParser.datasets.trigger_lists import Operation, ObjectState, Comparison, ObjectAttribute
from AoE2ScenarioParser.objects.data_objects.terrain_tile import TerrainTile
from AoE2ScenarioParser.objects.managers.trigger_manager import TriggerManager
from AoE2ScenarioParser.objects.support.area import Area
from AoE2ScenarioParser.objects.support.tile import Tile

from scenarios.lib.unit_modifier import UnitModifier


class ThunderFactory:

    def __init__(self, scenario, player_list, thunder_damage: int, time_to_sparks: int, time_to_lightning: int):
        self.scenario = scenario
        self.trigger_manager: TriggerManager = scenario.trigger_manager
        self.player_list = player_list
        self.thunder_damage = thunder_damage
        self.time_to_sparks = time_to_sparks
        self.time_to_lightning = time_to_lightning

    def set_thunder_flags(self):
        (UnitModifier(self.scenario, OtherInfo.FLAG_A.ID, PlayerId.GAIA)
         .modify_attribute(ObjectAttribute.STANDING_GRAPHIC, Operation.SET, 10636)
         .modify_attribute(ObjectAttribute.DYING_GRAPHIC, Operation.SET, 4151)
         .modify_attribute(ObjectAttribute.DEAD_UNIT_ID, Operation.SET, OtherInfo.FLAG_B.ID)
         .create_triggers()
         )
        (UnitModifier(self.scenario, OtherInfo.FLAG_B.ID, PlayerId.GAIA)
         .modify_attribute(ObjectAttribute.STANDING_GRAPHIC, Operation.SET, 10638)
         .modify_attribute(ObjectAttribute.HIT_POINTS, Operation.SET, 10)
         .create_triggers()
         )
        (UnitModifier(self.scenario, OtherInfo.FLAG_C.ID, PlayerId.GAIA)
         .modify_attribute(ObjectAttribute.STANDING_GRAPHIC, Operation.SET, 10637)
         .modify_attribute(ObjectAttribute.HIT_POINTS, Operation.SET, 2)
         .create_triggers()
         )
        (UnitModifier(self.scenario, OtherInfo.ROCK_FORMATION_2.ID, PlayerId.GAIA)
         .modify_attribute(ObjectAttribute.DEAD_UNIT_ID, Operation.SET, 143)
         .create_triggers()
         )

    def set_thunder_flag_damage(self):
        flag_damage = self.trigger_manager.add_trigger('Damage Flags', looping=True)
        flags = [OtherInfo.FLAG_A.ID, OtherInfo.FLAG_B.ID, OtherInfo.FLAG_C.ID]
        for flag in flags:
            flag_damage.new_effect.damage_object(
                source_player=PlayerId.GAIA,
                object_list_unit_id=flag,
                quantity=1
            )

    def set_thunder_zone(self, thunder_zone: Area, zone_id: int):
        init_variable = self.trigger_manager.add_trigger(f"Initialize Thunder Zone {zone_id}")
        init_variable.new_effect.change_variable(
            variable=zone_id,
            operation=Operation.SET,
            quantity=0
        )
        zone_with_units = self.trigger_manager.add_trigger(f"Thunder Zone {zone_id} Units", looping=True)
        zone_with_units.new_condition.variable_value(
            variable=zone_id,
            comparison=Comparison.LESS,
            quantity=0,
        )
        for player in self.player_list:
            zone_with_units.new_condition.or_()
            zone_with_units.new_condition.objects_in_area(
                quantity=1,
                source_player=player,
                area_x1=thunder_zone.x1,
                area_y1=thunder_zone.y1,
                area_x2=thunder_zone.x2,
                area_y2=thunder_zone.y2,
                object_state=ObjectState.ALIVE,
                inverted=False
            )
        zone_with_units.new_effect.change_variable(
            variable=zone_id,
            quantity=1,
            operation=Operation.ADD,
        )
        zone_empty = self.trigger_manager.add_trigger(f"Thunder Zone {zone_id} Empty", looping=True)
        zone_empty.new_condition.variable_value(
            variable=zone_id,
            comparison=Comparison.LARGER,
            quantity=0,
        )
        for player in self.player_list:
            zone_empty.new_condition.and_()
            zone_empty.new_condition.objects_in_area(
                quantity=1,
                source_player=player,
                area_x1=thunder_zone.x1,
                area_y1=thunder_zone.y1,
                area_x2=thunder_zone.x2,
                area_y2=thunder_zone.y2,
                object_state=ObjectState.ALIVE,
                inverted=True
            )
        zone_empty.new_effect.change_variable(
            variable=zone_id,
            quantity=1,
            operation=Operation.SUBTRACT,
        )

        # SPARKS
        sparks_step = 5
        for i, time in enumerate(range(self.time_to_sparks, self.time_to_lightning, sparks_step)):
            zone_sparks = self.trigger_manager.add_trigger(f"Thunder Zone Sparks {time}", looping=True)
            zone_sparks.new_condition.variable_value(
                variable=zone_id,
                comparison=Comparison.LARGER_OR_EQUAL,
                quantity=time,
            )
            zone_sparks.new_condition.variable_value(
                variable=zone_id,
                comparison=Comparison.LESS,
                quantity=time + sparks_step,
            )
            spark_tiles = self.get_even_distribution(thunder_zone, (i+1) * 3)
            for tile in spark_tiles:
                zone_sparks.new_effect.create_object(
                    source_player=PlayerId.GAIA,
                    object_list_unit_id=OtherInfo.FLAG_C.ID,
                    location_x=tile.x,
                    location_y=tile.y,
                )

        # LIGHTNING
        lightning = self.trigger_manager.add_trigger(f"Thunder Zone Lightning", looping=True)
        lightning.new_condition.variable_value(
            variable=zone_id,
            comparison=Comparison.EQUAL,
            quantity=self.time_to_lightning,
        )
        lightning.new_effect.change_variable(
            variable=zone_id,
            operation=Operation.SET,
            quantity=0
        )
        lightning_tiles = self.get_even_distribution(thunder_zone, 10)
        for tile in lightning_tiles:
            lightning.new_effect.create_object(
                source_player=PlayerId.GAIA,
                object_list_unit_id=OtherInfo.FLAG_A.ID,
                location_x=tile.x,
                location_y=tile.y,
            )
        for player in self.player_list:
            lightning.new_effect.damage_object(
                source_player=player,
                quantity=self.thunder_damage,
                area_x1=thunder_zone.x1,
                area_y1=thunder_zone.y1,
                area_x2=thunder_zone.x2,
                area_y2=thunder_zone.y2,
            )
        lightning.new_effect.kill_object(
            object_list_unit_id=OtherInfo.ROCK_FORMATION_2.ID,
            source_player=PlayerId.GAIA,
            area_x1=thunder_zone.x1,
            area_y1=thunder_zone.y1,
            area_x2=thunder_zone.x2,
            area_y2=thunder_zone.y2,
        )

    @staticmethod
    def get_even_distribution(thunder_area: Area, samples: int) -> list[Tile]:
        tiles = thunder_area.to_coords()
        selected = [random.choice(tiles)]

        remaining: set[None | Tile | TerrainTile] = set(tiles)
        remaining.remove(selected[0])

        while len(selected) < samples and remaining:

            best_tile = None
            best_dist = -1

            for tile in remaining:
                if not tile:
                    continue
                d = min(math.hypot(tile.x - s.x, tile.y - s.y) for s in selected)

                if d > best_dist:
                    best_dist = d
                    best_tile = tile

            selected.append(best_tile)
            remaining.remove(best_tile)

        return selected
