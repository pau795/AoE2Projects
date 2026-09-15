from AoE2ScenarioParser.datasets.buildings import BuildingInfo
from AoE2ScenarioParser.datasets.other import OtherInfo
from AoE2ScenarioParser.datasets.players import PlayerId
from AoE2ScenarioParser.datasets.trigger_lists import ObjectAttribute, Operation, GarrisonType, Attribute, ActionType, CombatAbility
from AoE2ScenarioParser.datasets.units import UnitInfo

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
        for unit in self.unit_manager.get_all_units():
            if unit.unit_const == UnitInfo.GREY_WOLF.ID:
                unit.unit_const = UnitInfo.DIRE_WOLF.ID


if __name__ == '__main__':
    template_class = Template(
        input_scenario_name=f'EDIT_AVALANCHE_1V1',
        output_scenario_name=f'EDIT_AVALANCHE_1V11',
    )
    template_class.convert()
