from AoE2ScenarioParser.datasets.techs import TechInfo
from AoE2ScenarioParser.datasets.trigger_lists import TechnologyState, Attribute, Operation
from AoE2ScenarioParser.datasets.units import UnitInfo
from AoE2ScenarioParser.objects.data_objects.trigger import Trigger
from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario


class CivSettings:
    STANDARD_FOOD = 200
    STANDARD_WOOD = 200
    STANDARD_STONE = 200
    STANDARD_GOLD = 100
    NOMAD_WOOD = 275
    NOMAD_STONE = 100
    APPLY_RESOURCES = False

    def __init__(self, scenario: AoE2DEScenario, player_id_list, nomad_players=None, delay=0):
        self.player_manager = scenario.player_manager
        self.trigger_manager = scenario.trigger_manager
        self.player_id_list = player_id_list
        self.nomad_players = nomad_players
        self.delay = delay
        for i, player_id in enumerate(self.player_id_list):

            gurjara_trigger = self.trigger_manager.add_trigger(f"Gurjara P{player_id}")
            aztec_trigger = self.trigger_manager.add_trigger(f"Aztec P{player_id}")
            maya_trigger = self.trigger_manager.add_trigger(f"Maya P{player_id}")
            inca_trigger = self.trigger_manager.add_trigger(f"Inca P{player_id}")
            musica_trigger = self.trigger_manager.add_trigger(f"Muisca P{player_id}")
            tupi_trigger = self.trigger_manager.add_trigger(f"Tupi P{player_id}")
            mapuche_trigger = self.trigger_manager.add_trigger(f"Mapuche P{player_id}")

            gurjara_trigger.new_condition.technology_state(
                source_player=player_id,
                technology=TechInfo.ELITE_CHAKRAM_THROWER.ID,
                quantity=TechnologyState.NOT_READY
            )
            gurjara_trigger.new_effect.replace_object(
                source_player=player_id,
                target_player=player_id,
                object_list_unit_id=UnitInfo.SCOUT_CAVALRY.ID,
                object_list_unit_id_2=UnitInfo.CAMEL_SCOUT.ID
            )

            aztec_trigger.new_condition.technology_state(
                source_player=player_id,
                technology=TechInfo.ELITE_JAGUAR_WARRIOR.ID,
                quantity=TechnologyState.NOT_READY
            )
            aztec_trigger.new_effect.replace_object(
                source_player=player_id,
                target_player=player_id,
                object_list_unit_id=UnitInfo.SCOUT_CAVALRY.ID,
                object_list_unit_id_2=UnitInfo.EAGLE_SCOUT.ID
            )
            maya_trigger.new_condition.technology_state(
                source_player=player_id,
                technology=TechInfo.ELITE_PLUMED_ARCHER.ID,
                quantity=TechnologyState.NOT_READY
            )
            maya_trigger.new_effect.replace_object(
                source_player=player_id,
                target_player=player_id,
                object_list_unit_id=UnitInfo.SCOUT_CAVALRY.ID,
                object_list_unit_id_2=UnitInfo.EAGLE_SCOUT.ID
            )
            inca_trigger.new_condition.technology_state(
                source_player=player_id,
                technology=TechInfo.ELITE_KAMAYUK.ID,
                quantity=TechnologyState.NOT_READY
            )
            inca_trigger.new_effect.replace_object(
                source_player=player_id,
                target_player=player_id,
                object_list_unit_id=UnitInfo.SCOUT_CAVALRY.ID,
                object_list_unit_id_2=UnitInfo.CHAMPI_SCOUT.ID
            )
            musica_trigger.new_condition.technology_state(
                source_player=player_id,
                technology=TechInfo.ELITE_GUECHA_WARRIOR.ID,
                quantity=TechnologyState.NOT_READY
            )
            musica_trigger.new_effect.replace_object(
                source_player=player_id,
                target_player=player_id,
                object_list_unit_id=UnitInfo.SCOUT_CAVALRY.ID,
                object_list_unit_id_2=UnitInfo.CHAMPI_SCOUT.ID
            )
            tupi_trigger.new_condition.technology_state(
                source_player=player_id,
                technology=TechInfo.ELITE_BLACKWOOD_ARCHER.ID,
                quantity=TechnologyState.NOT_READY
            )
            tupi_trigger.new_effect.replace_object(
                source_player=player_id,
                target_player=player_id,
                object_list_unit_id=UnitInfo.SCOUT_CAVALRY.ID,
                object_list_unit_id_2=UnitInfo.CHAMPI_SCOUT.ID
            )
            mapuche_trigger.new_condition.technology_state(
                source_player=player_id,
                technology=TechInfo.ELITE_KONA.ID,
                quantity=TechnologyState.NOT_READY
            )
            mapuche_trigger.new_effect.replace_object(
                source_player=player_id,
                target_player=player_id,
                object_list_unit_id=UnitInfo.SCOUT_CAVALRY.ID,
                object_list_unit_id_2=UnitInfo.CHAMPI_SCOUT.ID
            )

    def set_resources(self, civ_trigger: Trigger, initial_resources_trigger: Trigger, player_position: int, wood: int, food: int, gold: int, stone: int):
        player_id = self.player_id_list[player_position]
        is_nomad = self.nomad_players[player_position] if self.nomad_players else False
        wood = wood if not is_nomad else wood + self.NOMAD_WOOD
        stone = stone if not is_nomad else stone + self.NOMAD_STONE
        civ_trigger.new_effect.modify_resource(
            source_player=player_id,
            tribute_list=Attribute.FOOD_STORAGE,
            operation=Operation.ADD,
            quantity=food
        )
        civ_trigger.new_effect.modify_resource(
            source_player=player_id,
            tribute_list=Attribute.WOOD_STORAGE,
            operation=Operation.ADD,
            quantity=wood
        )
        civ_trigger.new_effect.modify_resource(
            source_player=player_id,
            tribute_list=Attribute.GOLD_STORAGE,
            operation=Operation.ADD,
            quantity=gold
        )
        civ_trigger.new_effect.modify_resource(
            source_player=player_id,
            tribute_list=Attribute.STONE_STORAGE,
            operation=Operation.ADD,
            quantity=stone
        )
        civ_trigger.new_effect.deactivate_trigger(trigger_id=initial_resources_trigger.trigger_id)
