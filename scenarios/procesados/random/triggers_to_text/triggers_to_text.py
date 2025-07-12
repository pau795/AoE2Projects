from scenarios.lib.parser_project import ParserProject


class TriggersToText(ParserProject):
    def __init__(self, input_scenario_name: str, output_file_name: str):
        super().__init__(input_scenario_name, "")
        self.output_file_name = output_file_name

    def process(self):
        manager = self.scenario.trigger_manager
        with open(f'output/{self.output_file_name}.txt', 'w', encoding='utf-8') as f:
            f.write(manager.get_content_as_string())


if __name__ == '__main__':
    scenario_name = 'ICE AGE TERRAZAS'
    triggers_to_text = TriggersToText(
        input_scenario_name=scenario_name,
        output_file_name=f'triggers_{scenario_name}'
    )
    triggers_to_text.process()


