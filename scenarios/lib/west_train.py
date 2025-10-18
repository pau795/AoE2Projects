from pathlib import Path
from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario

from scenarios.lib.utils import parametrize_xs


class WestTrainFactory:

    def __init__(self, scenario: AoE2DEScenario, train_player: int):
        self.scenario = scenario
        self.train_player = train_player
        module_dir = Path(__file__).parent
        xs_file = module_dir / "xs/west_train.xs"
        parametrized_xs = parametrize_xs(xs_file, {"train_player": str(train_player)})
        self.scenario.xs_manager.add_script(xs_string=parametrized_xs)

