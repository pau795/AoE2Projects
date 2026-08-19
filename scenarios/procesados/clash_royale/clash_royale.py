from scenarios.lib.parser_project import ParserProject


class ClashRoyale(ParserProject):

    def __init__(self, input_scenario_name: str, output_scenario_name: str):
        super().__init__(input_scenario_name, output_scenario_name)
        self.data_triggers = self.scenario.actions.load_data_triggers()
        self.trigger_manager = self.scenario.trigger_manager

    def process(self):
        
        pass