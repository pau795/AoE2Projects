import os
from abc import ABC, abstractmethod
from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario


class ParserProject(ABC):
    STEAM_ID = os.getenv('steam_id', 0)
    USER_FOLDER = f'{os.environ["USERPROFILE"]}'
    SCENARIO_FOLDER = f'{USER_FOLDER}\\Games\\Age of Empires 2 DE\\{STEAM_ID}\\resources\\_common\\scenario\\'

    def __init__(self, input_scenario_name, output_scenario_name, scenario=None):

        self.input_scenario_name = input_scenario_name
        self.output_scenario_name = output_scenario_name
        if scenario is None:
            self.input_file = f'{self.SCENARIO_FOLDER}{self.input_scenario_name}.aoe2scenario'
            self.output_file = f'{self.SCENARIO_FOLDER}{self.output_scenario_name}.aoe2scenario'
            self.scenario = AoE2DEScenario.from_file(self.input_file)
        else:
            self.scenario: AoE2DEScenario = scenario

    @abstractmethod
    def process(self):
        pass

    def convert(self):
        self.process()
        self.scenario.write_to_file(self.output_file)

    def load_scenario(self, scenario_name: str) -> AoE2DEScenario:
        input_file = f'{self.SCENARIO_FOLDER}{scenario_name}.aoe2scenario'
        return AoE2DEScenario.from_file(input_file)
