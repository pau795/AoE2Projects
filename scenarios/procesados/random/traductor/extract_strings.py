from AoE2ScenarioParser.datasets.effects import EffectId
from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario

import os

user_folder = f'{os.environ["USERPROFILE"]}'
steam_id = os.getenv('steam_id', 0)
scenario_folder = f'{user_folder}\\Games\\Age of Empires 2 DE\\{steam_id}\\resources\\_common\\scenario\\'
scenario_name = 'the age of clash royale'

input_file = f'{scenario_folder}{scenario_name}.aoe2scenario'
output_file = f'{scenario_folder}{scenario_name}_output.aoe2scenario'

scenario = AoE2DEScenario.from_file(input_file)
trigger_manager = scenario.trigger_manager
message_manager = scenario.message_manager

count = 707000

effect_list = [EffectId.CHANGE_OBJECT_NAME, EffectId.CHANGE_OBJECT_DESCRIPTION, EffectId.DISPLAY_TIMER,
               EffectId.CHANGE_OBJECT_PLAYER_NAME, EffectId.DISPLAY_INSTRUCTIONS, EffectId.SEND_CHAT]
msg2id = {}

instructions = message_manager.instructions.replace('\r', '\\n')
msg2id[instructions] = count
count += 1
message_manager.instructions = ""
message_manager.instructions_string_table_id = msg2id[instructions]

hints = message_manager.hints.replace('\r', '\\n')
msg2id[hints] = count
count += 1
message_manager.hints = ""
message_manager.hints_string_table_id = msg2id[hints]

for trigger in trigger_manager.triggers:
    if trigger.short_description:
        description = trigger.short_description.replace('\r', '\\n')
        if description not in msg2id:
            msg2id[description] = count
            count += 1
        trigger.short_description_stid = msg2id[description]
        trigger.short_description = ""
    for effect in trigger.effects:
        if effect.effect_type in effect_list:
            message = effect.message.replace('\r', '\\n')
            if message not in msg2id:
                msg2id[message] = count
                count += 1
            effect.string_id = msg2id[message]
            effect.message = ""

for k, v in msg2id.items():
    print(f'{v} "{k}"')

scenario.write_to_file(output_file)
