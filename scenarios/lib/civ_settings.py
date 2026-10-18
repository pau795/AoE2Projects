from AoE2ScenarioParser.datasets.object_support import Civilization
from AoE2ScenarioParser.datasets.techs import TechInfo
from AoE2ScenarioParser.datasets.trigger_lists import TechnologyState, Operation
from AoE2ScenarioParser.datasets.units import UnitInfo
from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario


class CivSettings:
    CIV_INFO = {
        Civilization.AZTECS: (TechInfo.ELITE_JAGUAR_WARRIOR.ID, UnitInfo.EAGLE_SCOUT.ID, (0, 0, 0, 50)),
        Civilization.MAYANS: (TechInfo.ELITE_PLUMED_ARCHER.ID, UnitInfo.EAGLE_SCOUT.ID, None),
        Civilization.INCAS: (TechInfo.ELITE_KAMAYUK.ID, UnitInfo.CHAMPI_SCOUT.ID, None),
        Civilization.MAPUCHE: (TechInfo.ELITE_KONA.ID, UnitInfo.CHAMPI_SCOUT.ID, None),
        Civilization.TUPI: (TechInfo.ELITE_BLACKWOOD_ARCHER.ID, UnitInfo.CHAMPI_SCOUT.ID, (25, 25, 25, 25)),
        Civilization.MUISCA: (TechInfo.ELITE_GUECHA_WARRIOR.ID, UnitInfo.CHAMPI_SCOUT.ID, None),
        Civilization.GURJARAS: (TechInfo.ELITE_CHAKRAM_THROWER.ID, UnitInfo.CAMEL_SCOUT.ID, None),
        Civilization.PERSIANS: (TechInfo.ELITE_WAR_ELEPHANT.ID, None, (50, 50, 0, 0)),
        Civilization.SICILIANS: (TechInfo.ELITE_SERJEANT.ID, None, (0, 0, 100, 0)),
    }

    def __init__(self, scenario: AoE2DEScenario, player_id_list, delay=0, change_scouts=True, add_resources=True):
        self.player_manager = scenario.player_manager
        self.trigger_manager = scenario.trigger_manager
        self.player_id_list = player_id_list
        self.add_resources = add_resources
        self.delay = delay

        for civ, (elite_tech, scout_unit, resources) in self.CIV_INFO.items():
            for i, player_id in enumerate(self.player_id_list):
                trigger = self.trigger_manager.add_trigger(f"{civ} P{player_id}")
                if delay > 0:
                    trigger.new_condition.timer(delay)
                trigger.new_condition.technology_state(
                    source_player=player_id,
                    technology=elite_tech,
                    quantity=TechnologyState.NOT_READY
                )
                if change_scouts and scout_unit is not None:
                    trigger.new_effect.replace_object(
                        source_player=player_id,
                        target_player=player_id,
                        object_list_unit_id=UnitInfo.SCOUT_CAVALRY.ID,
                        object_list_unit_id_2=scout_unit
                    )
                if add_resources and resources is not None:
                    for attribute, resource in enumerate(resources):
                        if resource != 0:
                            trigger.new_effect.modify_resource(
                                source_player=player_id,
                                tribute_list=attribute,
                                operation=Operation.ADD,
                                quantity=resource
                            )
