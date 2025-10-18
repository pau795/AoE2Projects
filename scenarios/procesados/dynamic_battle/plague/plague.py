import math
import random
from pathlib import Path

from AoE2ScenarioParser.datasets.players import PlayerId
from AoE2ScenarioParser.datasets.trigger_lists import AttackStance, ActionType
from AoE2ScenarioParser.datasets.units import UnitInfo
from AoE2ScenarioParser.objects.data_objects.trigger import Trigger
from AoE2ScenarioParser.objects.support.tile import Tile

from scenarios.lib.parser_project import ParserProject
from scenarios.lib.equally_probable_trigger_list import EquallyProbableTriggerList
from scenarios.lib.civ_settings import CivSettings


class Plague(ParserProject):

    def __init__(self, input_scenario_name: str, output_scenario_name: str):
        super().__init__(input_scenario_name, output_scenario_name)
        self.rino_life_time = 60
        self.plague_life_time = 60
        self.plague_units = 50
        self.plague_radius = 8
        self.init_plague_time = 730
        self.rino_sound = "RINO_MUERE_1"
        self.plague_sound = "MOSQUITO1"
        self.plague_unit = UnitInfo.FIRE_GALLEY.ID
        self.random_wait_periods = [120, 150, 180, 210, 240]
        self.player_list = [PlayerId.ONE, PlayerId.TWO]
        self.trigger_manager = self.scenario.trigger_manager
        self.map_manager = self.scenario.map_manager
        self.data_triggers = self.scenario.actions.load_data_triggers()

    def process(self):
        CivSettings(self.scenario, self.player_list)
        self.karambit_stats()
        plague_pond_list = []
        for tile in self.data_triggers.tiles["plague_ponds"]:
            plague_trigger = self.generate_plague_triggers(tile)
            plague_pond_list.append(plague_trigger)
        self.generate_plague_spawns(plague_pond_list)
        self.victory()

    def karambit_stats(self):
        module_dir = Path(__file__).parent
        xs_path = module_dir / "plague.xs"
        self.scenario.xs_manager.add_script(str(xs_path))
        horse_trigger = self.trigger_manager.add_trigger("Horse Trigger")
        horse_trigger.new_effect.disable_object_selection(
            source_player=PlayerId.THREE,
            object_list_unit_id=UnitInfo.HORSE_A.ID
        )
        horse_trigger.new_effect.disable_unit_targeting(
            source_player=PlayerId.THREE,
            object_list_unit_id=UnitInfo.HORSE_A.ID
        )
        plague_damage = self.trigger_manager.add_trigger("Plague Damage", looping=True)
        plague_damage.new_effect.damage_object(
            object_list_unit_id=self.plague_unit,
            source_player=PlayerId.THREE,
            quantity=1
        )
        plague_damage.new_effect.damage_object(
            object_list_unit_id=UnitInfo.RHINOCEROS.ID,
            source_player=PlayerId.GAIA,
            quantity=1
        )
        plague_damage.new_effect.remove_object(
            object_list_unit_id=self.plague_unit,
            source_player=PlayerId.THREE,
            area_x1=0,
            area_x2=self.map_manager.map_width - 1,
            area_y1=0,
            area_y2=0
        )
        plague_damage.new_effect.remove_object(
            object_list_unit_id=self.plague_unit,
            source_player=PlayerId.THREE,
            area_x1=self.map_manager.map_width - 1,
            area_x2=self.map_manager.map_width - 1,
            area_y1=0,
            area_y2=self.map_manager.map_height - 1
        )
        plague_damage.new_effect.remove_object(
            object_list_unit_id=self.plague_unit,
            source_player=PlayerId.THREE,
            area_x1=0,
            area_x2=self.map_manager.map_width - 1,
            area_y1=self.map_manager.map_height - 1,
            area_y2=self.map_manager.map_height - 1
        )
        plague_damage.new_effect.remove_object(
            object_list_unit_id=self.plague_unit,
            source_player=PlayerId.THREE,
            area_x1=0,
            area_x2=0,
            area_y1=0,
            area_y2=self.map_manager.map_height - 1
        )

    def generate_plague_triggers(self, pond_tile: Tile) -> Trigger:
        create_rino = self.trigger_manager.add_trigger("Create Plague Rino", enabled=False)
        create_rino.new_effect.create_object(
            object_list_unit_id=UnitInfo.RHINOCEROS.ID,
            source_player=PlayerId.GAIA,
            location_x=pond_tile.x,
            location_y=pond_tile.y
        )
        create_rino.new_effect.disable_unit_targeting(
            source_player=PlayerId.GAIA,
            object_list_unit_id=UnitInfo.RHINOCEROS.ID,
            area_x1=pond_tile.x - self.plague_radius,
            area_x2=pond_tile.x + self.plague_radius,
            area_y1=pond_tile.y - self.plague_radius,
            area_y2=pond_tile.y + self.plague_radius
        )
        for player in self.player_list:
            create_rino.new_effect.play_sound(
                source_player=player,
                sound_name=self.rino_sound
            )
        plague_units_tiles = self.get_plague_positions(pond_tile)
        create_delay = math.ceil(self.plague_life_time / len(plague_units_tiles))
        accumulated_delay = 0
        chunk_tiles = [plague_units_tiles[i:i + create_delay] for i in range(0, len(plague_units_tiles), create_delay)]
        for chunk in chunk_tiles:
            create_plague_trigger = self.trigger_manager.add_trigger(f"Create Plague", enabled=False)
            create_plague_trigger.new_condition.timer(timer=accumulated_delay)
            for plague_tile in chunk:
                create_plague_trigger.new_effect.create_object(
                    object_list_unit_id=self.plague_unit,
                    source_player=PlayerId.THREE,
                    location_x=plague_tile.x,
                    location_y=plague_tile.y
                )
            create_plague_trigger.new_effect.change_object_stance(
                object_list_unit_id=self.plague_unit,
                source_player=PlayerId.THREE,
                area_x1=pond_tile.x - self.plague_radius,
                area_x2=pond_tile.x + self.plague_radius,
                area_y1=pond_tile.y - self.plague_radius,
                area_y2=pond_tile.y + self.plague_radius,
                attack_stance=AttackStance.NO_ATTACK_STANCE
            )
            create_plague_trigger.new_effect.disable_unit_targeting(
                object_list_unit_id=self.plague_unit,
                source_player=PlayerId.THREE,
                area_x1=pond_tile.x - self.plague_radius,
                area_x2=pond_tile.x + self.plague_radius,
                area_y1=pond_tile.y - self.plague_radius,
                area_y2=pond_tile.y + self.plague_radius,
            )
            create_plague_trigger.new_effect.disable_object_selection(
                object_list_unit_id=self.plague_unit,
                source_player=PlayerId.THREE,
                area_x1=pond_tile.x - self.plague_radius,
                area_x2=pond_tile.x + self.plague_radius,
                area_y1=pond_tile.y - self.plague_radius,
                area_y2=pond_tile.y + self.plague_radius,
            )
            create_rino.new_effect.activate_trigger(create_plague_trigger.trigger_id)
            accumulated_delay += create_delay
        plague_attack_trigger = self.trigger_manager.add_trigger("Plague Attack", enabled=False)
        for plague_tile in plague_units_tiles:
            attack_vector = [plague_tile.x - pond_tile.x, plague_tile.y - pond_tile.y]
            distance = (math.sqrt(attack_vector[0] ** 2 + attack_vector[1] ** 2))
            normal_vector = (attack_vector[0] / distance, attack_vector[1] / distance)
            x, y = plague_tile.x, plague_tile.y
            while 0 <= x < self.map_manager.map_width and 0 <= y < self.map_manager.map_height:
                x += normal_vector[0]
                y += normal_vector[1]
            x = int(x - normal_vector[0])
            y = int(y - normal_vector[1])
            plague_attack_trigger.new_effect.task_object(
                object_list_unit_id=self.plague_unit,
                source_player=PlayerId.THREE,
                area_x1=plague_tile.x,
                area_y1=plague_tile.y,
                area_x2=plague_tile.x,
                area_y2=plague_tile.y,
                location_x=x,
                location_y=y,
                action_type=ActionType.ATTACK_MOVE
            )

        rino_dead_trigger = self.trigger_manager.add_trigger("Plague Rino Dead", enabled=False)
        rino_dead_trigger.new_condition.own_fewer_objects(
            object_list=UnitInfo.RHINOCEROS.ID,
            source_player=PlayerId.GAIA,
            quantity=0,
            area_x1=pond_tile.x - self.plague_radius,
            area_x2=pond_tile.x + self.plague_radius,
            area_y1=pond_tile.y - self.plague_radius,
            area_y2=pond_tile.y + self.plague_radius
        )
        rino_dead_trigger.new_effect.change_object_stance(
            source_player=PlayerId.THREE,
            object_list_unit_id=self.plague_unit,
            area_x1=pond_tile.x - self.plague_radius,
            area_x2=pond_tile.x + self.plague_radius,
            area_y1=pond_tile.y - self.plague_radius,
            area_y2=pond_tile.y + self.plague_radius,
            attack_stance=AttackStance.AGGRESSIVE_STANCE
        )
        for player in self.player_list:
            rino_dead_trigger.new_effect.play_sound(
                source_player=player,
                sound_name=self.plague_sound
            )
        rino_dead_trigger.new_effect.activate_trigger(trigger_id=plague_attack_trigger.trigger_id)
        create_rino.new_effect.activate_trigger(rino_dead_trigger.trigger_id)

        return create_rino

    def get_plague_positions(self, tile: Tile) -> list[Tile]:
        num_circles = int(math.sqrt(self.plague_units))
        radius_increment = self.plague_radius / num_circles
        items = []
        shift = 0
        total_circumference_length = sum((i + 1) for i in range(num_circles))
        for i in range(num_circles):
            r = radius_increment * (i + 1)
            num_items = int(self.plague_units * (i + 1) / total_circumference_length)
            for j in range(num_items):
                angle = math.radians(360 / num_items * j + shift)
                x = int(tile.x + r * math.cos(angle))
                y = int(tile.y + r * math.sin(angle))
                items.append(Tile(x, y))
                shift += random.randint(-10, 10)
        return items

    def generate_plague_spawns(self, plague_pond_list: list[Trigger]):
        no_karambits = self.trigger_manager.add_trigger("No Karambits", enabled=False)

        spawn_a = self.trigger_manager.add_trigger("Plague Spawn A", enabled=False)
        spawn_a.new_effect.activate_trigger(trigger_id=plague_pond_list[3].trigger_id)
        spawn_a.new_effect.activate_trigger(trigger_id=plague_pond_list[4].trigger_id)
        spawn_a.new_effect.activate_trigger(trigger_id=plague_pond_list[5].trigger_id)

        spawn_b = self.trigger_manager.add_trigger("Plague Spawn B", enabled=False)
        spawn_b.new_effect.activate_trigger(trigger_id=plague_pond_list[1].trigger_id)
        spawn_b.new_effect.activate_trigger(trigger_id=plague_pond_list[2].trigger_id)
        spawn_b.new_effect.activate_trigger(trigger_id=plague_pond_list[6].trigger_id)
        spawn_b.new_effect.activate_trigger(trigger_id=plague_pond_list[7].trigger_id)

        spawn_c = self.trigger_manager.add_trigger("Plague Spawn C", enabled=False)
        spawn_c.new_effect.activate_trigger(trigger_id=plague_pond_list[0].trigger_id)
        spawn_c.new_effect.activate_trigger(trigger_id=plague_pond_list[3].trigger_id)
        spawn_c.new_effect.activate_trigger(trigger_id=plague_pond_list[5].trigger_id)

        spawn_d = self.trigger_manager.add_trigger("Plague Spawn D", enabled=False)
        spawn_d.new_effect.activate_trigger(trigger_id=plague_pond_list[0].trigger_id)
        spawn_d.new_effect.activate_trigger(trigger_id=plague_pond_list[4].trigger_id)

        random_spawn = EquallyProbableTriggerList(self.trigger_manager, [spawn_a, spawn_b, spawn_c, spawn_d], "Plague Spawns")
        random_spawn.enable_probability_trigger.new_effect.activate_trigger(trigger_id=no_karambits.trigger_id)

        period_triggers = []
        for i, period in enumerate(self.random_wait_periods):
            period_trigger = self.trigger_manager.add_trigger(f"Plague Period {i}", looping=False, enabled=False)
            period_trigger.new_condition.timer(timer=period)
            period_trigger.new_effect.activate_trigger(trigger_id=random_spawn.enable_probability_trigger.trigger_id)
            period_triggers.append(period_trigger)

        random_periods = EquallyProbableTriggerList(self.trigger_manager, period_triggers, "Plague Periods")

        no_karambits.new_condition.timer(timer=self.rino_life_time)
        no_karambits.new_condition.own_fewer_objects(object_list=self.plague_unit, source_player=PlayerId.THREE, quantity=0)
        no_karambits.new_effect.activate_trigger(trigger_id=random_periods.enable_probability_trigger.trigger_id)

        init_plague = self.trigger_manager.add_trigger("Init Plague", enabled=True)
        init_plague.new_condition.timer(timer=self.init_plague_time)
        init_plague.new_effect.activate_trigger(trigger_id=random_spawn.enable_probability_trigger.trigger_id)

    def victory(self):
        for player in self.player_list:
            player_defeat = self.trigger_manager.add_trigger(f"Defeat player {player}", enabled=True)
            player_defeat.new_condition.player_defeated(source_player=player)
            player_defeat.new_effect.declare_victory(source_player=PlayerId.THREE, enabled=False)


if __name__ == "__main__":
    plaga = Plague(
        input_scenario_name='EDIT_PLAGUE_1V1',
        output_scenario_name='OUTPUT_PLAGUE_1V1',
    )
    plaga.convert()
