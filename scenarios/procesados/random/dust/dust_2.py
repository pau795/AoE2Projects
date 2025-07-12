from AoE2ScenarioParser.datasets.other import OtherInfo

from scenarios.lib.parser_project import ParserProject
from AoE2ScenarioParser.datasets.players import PlayerId


class Dust2(ParserProject):

    def __init__(self, input_scenario_name: str, output_scenario_name: str):
        super().__init__(input_scenario_name, output_scenario_name)

    def process(self):
        trigger_manager = self.scenario.trigger_manager
        create_revealers = trigger_manager.add_trigger("Create Revealers")
        for x in range(0, self.scenario.map_manager.map_width, 15):
            for y in range(0, self.scenario.map_manager.map_height, 15):
                for player in [PlayerId.ONE, PlayerId.TWO, PlayerId.THREE, PlayerId.FOUR, PlayerId.FIVE,
                               PlayerId.SIX, PlayerId.SEVEN, PlayerId.EIGHT]:
                    create_revealers.new_effect.create_object(
                        object_list_unit_id=OtherInfo.MAP_REVEALER_GIANT.ID,
                        location_x=x,
                        location_y=y,
                        source_player=player
                    )
        map_area = self.scenario.new.area().select_entire_map()
        remove_revealers = trigger_manager.add_trigger("Remove Revealers")
        remove_revealers.new_condition.timer(timer=3)
        for player in [PlayerId.ONE, PlayerId.TWO, PlayerId.THREE, PlayerId.FOUR, PlayerId.FIVE,
                       PlayerId.SIX, PlayerId.SEVEN, PlayerId.EIGHT]:
            remove_revealers.new_effect.remove_object(
                object_list_unit_id=OtherInfo.MAP_REVEALER_GIANT.ID,
                area_x1=map_area.x1,
                area_y1=map_area.y1,
                area_x2=map_area.x2,
                area_y2=map_area.y2,
                source_player=player
            )
        pass


dust = Dust2(
    input_scenario_name='DUST',
    output_scenario_name='DUST_output'
)
dust.convert()
