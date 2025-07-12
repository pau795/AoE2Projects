import random

from AoE2ScenarioParser.datasets.other import OtherInfo
from AoE2ScenarioParser.datasets.players import PlayerId
from AoE2ScenarioParser.datasets.trigger_lists import ObjectClass, ObjectAttribute, Operation, PanelLocation
from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario

from scenarios.lib.random_probability import EqualRandomProbability


class EarthquakeFactory:

    def __init__(self, scenario: AoE2DEScenario, initial_delay, warning_delay, earthquake_duration, period_list,
                 damage, area_list, crack_sound, earthquake_sound, player_list):
        self.scenario = scenario
        self.trigger_manager = scenario.trigger_manager
        self.initial_delay = initial_delay
        self.warning_delay = warning_delay
        self.earthquake_duration = earthquake_duration
        self.period_list = period_list
        self.earthquake_damage = damage
        self.area_list = area_list
        self.crack_sound = crack_sound
        self.earthquake_sound = earthquake_sound
        self.player_list = player_list
        self.generate_earthquakes()

    def generate_earthquakes(self):
        crack_terrain = self.trigger_manager.add_trigger("Crack Terrain", looping=False, enabled=True)
        initial_delay = self.trigger_manager.add_trigger("Initial Delay", looping=False, enabled=True)
        cracks = self.trigger_manager.add_trigger("Crack Warning", looping=False, enabled=False)
        crack_warning_duration = self.trigger_manager.add_trigger("Crack Warning Duration", looping=False, enabled=False)
        earthquake_damage = self.trigger_manager.add_trigger("Earthquake Damage", looping=True, enabled=False)
        earthquake_duration = self.trigger_manager.add_trigger("Earthquake Duration", looping=False, enabled=False)

        crack_terrain.new_effect.modify_attribute(
                object_list_unit_id=OtherInfo.CRACKS.ID,
                source_player=PlayerId.GAIA,
                object_attributes=ObjectAttribute.TERRAIN_RESTRICTION_ID,
                operation=Operation.SET,
                quantity=4
            )

        # initial delay
        initial_delay.new_condition.timer(
            timer=self.initial_delay
        )
        initial_delay.new_effect.activate_trigger(
            trigger_id=cracks.trigger_id
        )

        # cracks
        for area in self.area_list:
            for tile in area.to_coords(as_terrain=True):
                if random.randint(0, 15) == 0:
                    cracks.new_effect.create_object(
                        source_player=PlayerId.GAIA,
                        object_list_unit_id=OtherInfo.CRACKS.ID,
                        location_x=tile.x,
                        location_y=tile.y,
                    )
        cracks.new_effect.display_instructions(
            object_list_unit_id=OtherInfo.STONE_MINE.ID,
            source_player=PlayerId.GAIA,
            sound_name=self.crack_sound,
            message="The ground breaks up!",
            display_time=20,
            instruction_panel_position=PanelLocation.BOTTOM
        )
        cracks.new_effect.activate_trigger(
            trigger_id=crack_warning_duration.trigger_id
        )

        # crack warning delay
        crack_warning_duration.new_condition.timer(
            timer=self.warning_delay
        )
        crack_warning_duration.new_effect.display_instructions(
            object_list_unit_id=OtherInfo.STONE_MINE.ID,
            source_player=PlayerId.GAIA,
            sound_name=self.earthquake_sound,
            message="EARTHQUAKE!",
            display_time=20,
            instruction_panel_position=PanelLocation.BOTTOM
        )
        crack_warning_duration.new_effect.activate_trigger(
            trigger_id=earthquake_damage.trigger_id
        )
        crack_warning_duration.new_effect.activate_trigger(
            trigger_id=earthquake_duration.trigger_id
        )
        crack_warning_duration.new_effect.remove_object(
            source_player=PlayerId.GAIA,
            object_list_unit_id=OtherInfo.ROCK_FORMATION_3.ID,
        )

        # earthquake damage
        for area in self.area_list:
            for player in self.player_list:
                earthquake_damage.new_effect.damage_object(
                    source_player=player,
                    area_x1=area.x1,
                    area_y1=area.y1,
                    area_x2=area.x2,
                    area_y2=area.y2,
                    quantity=self.earthquake_damage,
                    object_group=ObjectClass.BUILDING
                )
                earthquake_damage.new_effect.damage_object(
                    source_player=player,
                    area_x1=area.x1,
                    area_y1=area.y1,
                    area_x2=area.x2,
                    area_y2=area.y2,
                    quantity=self.earthquake_damage,
                    object_group=ObjectClass.TOWER
                )
                earthquake_damage.new_effect.damage_object(
                    source_player=player,
                    area_x1=area.x1,
                    area_y1=area.y1,
                    area_x2=area.x2,
                    area_y2=area.y2,
                    quantity=self.earthquake_damage,
                    object_group=ObjectClass.WALL
                )

        # earthquake period
        period_triggers = []
        for i, period in enumerate(self.period_list):
            period_trigger = self.trigger_manager.add_trigger(f"Earthquake Period {i}", looping=False, enabled=False)
            period_trigger.new_condition.timer(
                timer=period
            )
            period_trigger.new_effect.activate_trigger(
                trigger_id=cracks.trigger_id
            )
            period_triggers.append(period_trigger)

        probability_trigger = EqualRandomProbability(self.trigger_manager, period_triggers, "Earthquake Period")

        # earthquake duration
        earthquake_duration.new_condition.timer(
            timer=self.earthquake_duration
        )
        for area in self.area_list:
            earthquake_duration.new_effect.remove_object(
                source_player=PlayerId.GAIA,
                object_list_unit_id=OtherInfo.CRACKS.ID,
                area_x1=area.x1,
                area_y1=area.y1,
                area_x2=area.x2,
                area_y2=area.y2,
            )
        earthquake_duration.new_effect.deactivate_trigger(
            trigger_id=earthquake_damage.trigger_id
        )
        earthquake_duration.new_effect.activate_trigger(
            trigger_id=probability_trigger.enable_probability_trigger.trigger_id
        )
