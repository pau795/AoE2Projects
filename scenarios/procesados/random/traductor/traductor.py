import re

from AoE2ScenarioParser.datasets.effects import EffectId
from AoE2ScenarioParser.datasets.trigger_lists import ObjectAttribute

from scenarios.lib.parser_project import ParserProject


class TranslateScenario(ParserProject):

    def __init__(self, input_scenario_name: str, output_scenario_name: str, strings_file_path: str):
        super().__init__(input_scenario_name, output_scenario_name)
        self.strings_file_path = strings_file_path

    def process(self):
        pass
        trigger_manager = self.scenario.trigger_manager
        message_manager = self.scenario.message_manager

        string_dict = self.obtain_string_dict()
        effect_list = [EffectId.CHANGE_OBJECT_NAME, EffectId.CHANGE_OBJECT_DESCRIPTION, EffectId.DISPLAY_TIMER,
                       EffectId.CHANGE_OBJECT_PLAYER_NAME, EffectId.DISPLAY_INSTRUCTIONS, EffectId.SEND_CHAT]

        message_manager.instructions = string_dict[message_manager.instructions_string_table_id]
        message_manager.instructions_string_table_id = 4294967294

        message_manager.hints = string_dict[message_manager.hints_string_table_id]
        message_manager.hints_string_table_id = 4294967294

        for trigger in trigger_manager.triggers:
            if trigger.short_description_stid != 0:
                trigger.short_description = string_dict[trigger.short_description_stid]
                trigger.short_description_stid = 0
            for effect in trigger.effects:
                if effect.effect_type in effect_list:
                    effect.message = string_dict[effect.string_id]
                    effect.string_id = -1
                elif effect.effect_type == EffectId.MODIFY_ATTRIBUTE and effect.object_attributes == ObjectAttribute.OBJECT_NAME_ID:
                    trigger.remove_effect(effect=effect)

    def obtain_string_dict(self) -> {int: str}:
        string_dict = {}
        regex = re.compile(r'(\d+)\s\"(.*)\"')
        with open(self.strings_file_path, 'r', encoding='utf-8') as f:
            for line in f:
                match = regex.match(line)
                if match:
                    string_dict[int(match.group(1))] = match.group(2).replace('\\n', '\n')
        return string_dict


clash = TranslateScenario(
    input_scenario_name='the age of clash royale',
    output_scenario_name='ES the age of clash royale',
    strings_file_path='output/key-value-modded-strings-utf8.txt'
)
clash.convert()
