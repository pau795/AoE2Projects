from AoE2ScenarioParser.datasets.players import PlayerId

from scenarios.lib.parser_project import ParserProject
from scenarios.lib.civ_settings import CivSettings
from scenarios.lib.vulkan_factory import VulkanFactory


class VulkanMultiplayer(ParserProject):

    def __init__(self, input_scenario_name: str, output_scenario_name: str):
        super().__init__(input_scenario_name, output_scenario_name)
        self.first_stage_time = 600
        self.second_stage_time = 1200
        self.explosion_period = 130
        self.lava_damage = 30
        self.volcan_sound = "volcan"
        self.player_list = [PlayerId.ONE, PlayerId.TWO, PlayerId.THREE, PlayerId.FOUR, PlayerId.FIVE, PlayerId.SIX, PlayerId.SEVEN, PlayerId.EIGHT]

    def process(self):
        try:
            CivSettings(self.scenario, self.player_list)
            VulkanFactory(
                scenario=self.scenario,
                first_stage_time=self.first_stage_time,
                second_stage_time=self.second_stage_time,
                explosion_period=self.explosion_period,
                lava_damage=self.lava_damage,
                volcan_sound=self.volcan_sound,
                player_list=self.player_list
            )
        except Exception as e:
            raise e


if __name__ == '__main__':
    vulkan_class = VulkanMultiplayer(
        input_scenario_name='EDIT_VULKAN_4V4',
        output_scenario_name='OUTPUT_VULKAN_4V4'
    )
    vulkan_class.convert()
