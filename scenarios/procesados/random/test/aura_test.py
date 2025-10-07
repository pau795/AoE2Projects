from AoE2ScenarioParser.objects.data_objects.trigger import Trigger

from scenarios.lib.parser_project import ParserProject


class Test1(ParserProject):

    def __init__(self, input_scenario_name: str, output_scenario_name: str):
        super().__init__(input_scenario_name, output_scenario_name)
        self.trigger_manager = self.scenario.trigger_manager
        self.map_manager = self.scenario.map_manager
        self.unit_manager = self.scenario.unit_manager
        self.xs_manager = self.scenario.xs_manager

    def process(self):
        # REALIZAR LOS CAMBIOS DEL ESCENARIO AQUÍ

        pass


if __name__ == '__main__':
    test1 = Test1(
        input_scenario_name=f'aura_test',
        output_scenario_name=f'aura_test_output'
    )
    test1.convert()
