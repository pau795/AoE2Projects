import os

from AoE2ScenarioParser.datasets.buildings import BuildingInfo
from AoE2ScenarioParser.datasets.players import PlayerId
from AoE2ScenarioParser.datasets.trigger_lists import ObjectAttribute, Operation
from AoE2ScenarioParser.datasets.units import UnitInfo
from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario

user_folder = f'{os.environ["USERPROFILE"]}'
steam_id = os.getenv('steam_id', 0)
scenario_folder = f'{user_folder}\\Games\\Age of Empires 2 DE\\{steam_id}\\resources\\_common\\scenario\\'


def generate_base_scenario():
    scenario_name = 'empty1'
    input_file = f'{scenario_folder}{scenario_name}.aoe2scenario'
    base_file = f'{scenario_folder}test_modify_effect_base.aoe2scenario'

    scenario = AoE2DEScenario.from_file(input_file)
    unit_manager = scenario.unit_manager
    map_manager = scenario.map_manager
    unit_manager.add_unit(
        unit_const=BuildingInfo.BARRACKS.ID,
        player=PlayerId.TWO,
        x=map_manager.map_width // 2,
        y=map_manager.map_height // 2,
        z=0
    )

    unit_manager.add_unit(
        unit_const=UnitInfo.CROSSBOWMAN.ID,
        player=PlayerId.ONE,
        x=map_manager.map_width // 2 - 5,
        y=map_manager.map_height // 2,
        z=0
    )
    scenario.write_to_file(base_file)


def generate_parser_scenario():
    scenario_name = 'empty1'
    input_file = f'{scenario_folder}{scenario_name}.aoe2scenario'
    base_file = f'{scenario_folder}test_modify_effect_paser.aoe2scenario'

    scenario = AoE2DEScenario.from_file(input_file)
    trigger_manager = scenario.trigger_manager
    unit_manager = scenario.unit_manager
    map_manager = scenario.map_manager
    unit_manager.add_unit(
        unit_const=BuildingInfo.BARRACKS.ID,
        player=PlayerId.TWO,
        x=map_manager.map_width // 2,
        y=map_manager.map_height // 2,
        z=0
    )

    unit_manager.add_unit(
        unit_const=UnitInfo.CROSSBOWMAN.ID,
        player=PlayerId.ONE,
        x=map_manager.map_width // 2 - 5,
        y=map_manager.map_height // 2,
        z=0
    )
    trigger = trigger_manager.add_trigger('modify attr')
    trigger.new_effect.modify_attribute(
        source_player=PlayerId.ONE,
        object_list_unit_id=364,
        object_attributes=ObjectAttribute.STANDING_GRAPHIC,
        operation=Operation.SET,
        quantity=2575,
    )
    scenario.write_to_file(base_file)


def compare_scenarios():
    editor_scenario_path = f'{scenario_folder}test_modify_effect_scenario_editor.aoe2scenario'
    parser_scenario_path = f'{scenario_folder}test_modify_effect_paser.aoe2scenario'

    editor_scenario = AoE2DEScenario.from_file(editor_scenario_path)
    parser_scenario = AoE2DEScenario.from_file(parser_scenario_path)

    editor_trigger_manager = editor_scenario.trigger_manager
    parser_trigger_manager = parser_scenario.trigger_manager
    print("SCENARIO EDITOR TRIGGERS---------------------------:")
    print(editor_trigger_manager.get_content_as_string())
    print("SCENARIO PARSER TRIGGERS---------------------------:")
    print(parser_trigger_manager.get_content_as_string())


if __name__ == '__main__':
    # generate_parser_scenario()
    compare_scenarios()


