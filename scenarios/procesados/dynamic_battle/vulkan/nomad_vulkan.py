from AoE2ScenarioParser.datasets.players import PlayerId

from scenarios.lib.nomad_start import NomadStart
from scenarios.lib.parser_project import ParserProject
from scenarios.lib.vulkan_factory import VulkanFactory


class NomadVulkan(ParserProject):

    def __init__(self, input_scenario_name: str, output_scenario_name: str):
        super().__init__(input_scenario_name, output_scenario_name)
        self.first_stage_time = 600
        self.second_stage_time = 1200
        self.explosion_period = 130
        self.lava_damage = 30
        self.volcan_sound = 'volcan'
        self.player_list = [PlayerId.ONE, PlayerId.TWO]

    def process(self):
        try:
            trigger_manager = self.scenario.trigger_manager
            trigger_data = self.scenario.actions.load_data_triggers()
            NomadStart(trigger_manager, trigger_data, self.player_list)
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
    nomad_vulkan = NomadVulkan(
        input_scenario_name='VULKAN NOMADA',
        output_scenario_name='VULKAN NOMADA output',
    )
    nomad_vulkan.convert()
