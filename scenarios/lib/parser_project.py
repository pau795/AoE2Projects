import os
from abc import ABC, abstractmethod
from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario


class ParserProject(ABC):

    def __init__(self, input_scenario_name, output_scenario_name, scenario=None):
        self.steam_id = os.getenv('steam_id', 0)
        self.input_scenario_name = input_scenario_name
        self.output_scenario_name = output_scenario_name
        if scenario is None:
            user_folder = f'{os.environ["USERPROFILE"]}'
            scenario_folder = f'{user_folder}\\Games\\Age of Empires 2 DE\\{self.steam_id}\\resources\\_common\\scenario\\'
            self.input_file = f'{scenario_folder}{self.input_scenario_name}.aoe2scenario'
            self.output_file = f'{scenario_folder}{self.output_scenario_name}.aoe2scenario'
            self.scenario = AoE2DEScenario.from_file(self.input_file)
        else:
            self.scenario: AoE2DEScenario = scenario

    @abstractmethod
    def process(self):
        pass

    def convert(self):
        self.process()
        self.scenario.write_to_file(self.output_file)
