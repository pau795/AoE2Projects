from AoE2ScenarioParser.datasets.buildings import BuildingInfo
from AoE2ScenarioParser.datasets.other import OtherInfo
from AoE2ScenarioParser.datasets.players import PlayerId
from AoE2ScenarioParser.datasets.trigger_lists import ObjectAttribute, Operation, GarrisonType, Attribute, ActionType, CombatAbility
from AoE2ScenarioParser.datasets.units import UnitInfo
from AoE2ScenarioParser.objects.support.trigger_select import TriggerSelect

from scenarios.lib.parser_project import ParserProject
from scenarios.lib.unit_modifier import UnitModifier
from scenarios.lib.xs.unit_tasks import AuraTask, TaskTargets
from scenarios.lib.xs.xs_constants import XsConstantObjectClass, XsConstantAttribute, XsConstantEffectAmount


class Template(ParserProject):

    def __init__(self, input_scenario_name: str, output_scenario_name: str):
        super().__init__(input_scenario_name, output_scenario_name)
        self.trigger_manager = self.scenario.trigger_manager
        self.map_manager = self.scenario.map_manager
        self.unit_manager = self.scenario.unit_manager
        self.xs_manager = self.scenario.xs_manager

    def process(self):

        old_jumanji = self.load_scenario("EDIT_JUMANJI_1V1")
        for tile in old_jumanji.new.area().select_entire_map().to_coords(as_terrain=True):
            new_tile = self.map_manager.get_tile(tile.x, tile.y)
            new_tile.terrain_id = tile.terrain_id
            new_tile.layer = tile.layer
            new_tile.elevation = tile.elevation

        for unit in old_jumanji.unit_manager.get_all_units():
            self.scenario.unit_manager.clone_unit(unit)

        for trigger in old_jumanji.trigger_manager.triggers:
            self.trigger_manager.add_trigger(
                name=trigger.name,
                description=trigger.description,
                description_stid=trigger.description_stid,
                display_as_objective=trigger.display_as_objective,
                short_description=trigger.short_description,
                short_description_stid=trigger.short_description_stid,
                display_on_screen=trigger.display_on_screen,
                description_order=trigger.description_order,
                enabled=trigger.enabled,
                looping=trigger.looping,
                execute_on_load=trigger.execute_on_load,
                header=trigger.header,
                mute_objectives=trigger.mute_objectives,
                conditions=trigger.conditions,
                effects=trigger.effects,

            )


if __name__ == '__main__':
    template_class = Template(
        input_scenario_name=f'NEW_JUMANJI_1V1',
        output_scenario_name=f'NEW_JUMANJI_1V1_2',
    )
    template_class.convert()
