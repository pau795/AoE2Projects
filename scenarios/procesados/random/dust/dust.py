from scenarios.lib.parser_project import ParserProject
from AoE2ScenarioParser.datasets.players import PlayerId
from AoE2ScenarioParser.datasets.trigger_lists import Comparison


class Dust(ParserProject):

    def __init__(self, input_scenario_name: str, output_scenario_name: str):
        super().__init__(input_scenario_name, output_scenario_name)

    def process(self):
        trigger_manager = self.scenario.trigger_manager
        trigger_data = self.scenario.actions.load_data_triggers(remove_template_triggers=False)
        areas_team1 = trigger_data.areas['e1']
        areas_team2 = trigger_data.areas['e2']

        area_dict = {
            PlayerId.ONE: areas_team1,
            PlayerId.TWO: areas_team1,
            PlayerId.THREE: areas_team1,
            PlayerId.FOUR: areas_team1,
            PlayerId.FIVE: areas_team2,
            PlayerId.SIX: areas_team2,
            PlayerId.SEVEN: areas_team2,
            PlayerId.EIGHT: areas_team2
        }

        trigger_manager.add_trigger("==========")

        for player in area_dict.keys():
            # trabuco
            trabuco = trigger_manager.add_trigger(f'Trabuco P{player.value}', looping=True, enabled=True)
            trabuco.new_condition.objects_in_area(
                source_player=player,
                area_x1=area_dict[player][0].x1,
                area_y1=area_dict[player][0].y1,
                area_x2=area_dict[player][0].x2,
                area_y2=area_dict[player][0].y2,
                quantity=1
            )
            trabuco.new_condition.variable_value(
                variable=30,
                quantity=1,
                comparison=Comparison.EQUAL
            )
            trabuco.new_effect.script_call(
                message=f'trabuco_p{player.value}()'
            )

            # Escopeta

            escopeta = trigger_manager.add_trigger(f'Escopeta P{player.value}', looping=True, enabled=True)
            escopeta.new_condition.objects_in_area(
                source_player=player,
                area_x1=area_dict[player][1].x1,
                area_y1=area_dict[player][1].y1,
                area_x2=area_dict[player][1].x2,
                area_y2=area_dict[player][1].y2,
                quantity=1
            )
            escopeta.new_condition.variable_value(
                variable=30,
                quantity=1,
                comparison=Comparison.EQUAL
            )
            escopeta.new_effect.script_call(
                message=f'escopeta_p{player.value}()'
            )

            # Lanzagranadas

            lanzagranadas = trigger_manager.add_trigger(f'Lanzagranadas P{player.value}', looping=True, enabled=True)
            lanzagranadas.new_condition.objects_in_area(
                source_player=player,
                area_x1=area_dict[player][2].x1,
                area_y1=area_dict[player][2].y1,
                area_x2=area_dict[player][2].x2,
                area_y2=area_dict[player][2].y2,
                quantity=1
            )
            lanzagranadas.new_condition.variable_value(
                variable=30,
                quantity=1,
                comparison=Comparison.EQUAL
            )
            lanzagranadas.new_effect.script_call(
                message=f'lanzagranadas_p{player.value}()'
            )
            # Sniper

            sniper = trigger_manager.add_trigger(f'Sniper P{player.value}', looping=True, enabled=True)
            sniper.new_condition.objects_in_area(
                source_player=player,
                area_x1=area_dict[player][3].x1,
                area_y1=area_dict[player][3].y1,
                area_x2=area_dict[player][3].x2,
                area_y2=area_dict[player][3].y2,
                quantity=1
            )
            sniper.new_condition.variable_value(
                variable=30,
                quantity=1,
                comparison=Comparison.EQUAL
            )
            sniper.new_effect.script_call(
                message=f'sniper_p{player.value}()'
            )
            # metralleta

            metralleta = trigger_manager.add_trigger(f'metralleta P{player.value}', looping=True, enabled=True)
            metralleta.new_condition.objects_in_area(
                source_player=player,
                area_x1=area_dict[player][4].x1,
                area_y1=area_dict[player][4].y1,
                area_x2=area_dict[player][4].x2,
                area_y2=area_dict[player][4].y2,
                quantity=1
            )
            metralleta.new_condition.variable_value(
                variable=30,
                quantity=1,
                comparison=Comparison.EQUAL
            )
            metralleta.new_effect.script_call(
                message=f'metralleta_p{player.value}()'
            )

            trigger_manager.add_trigger("==========")
        pass


dust = Dust(
    input_scenario_name='DUST',
    output_scenario_name='DUST_output'
)
dust.convert()
