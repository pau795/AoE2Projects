from AoE2ScenarioParser.datasets.other import OtherInfo
from AoE2ScenarioParser.datasets.players import PlayerId
from AoE2ScenarioParser.objects.managers.trigger_manager import TriggerManager
from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario
from AoE2ScenarioParser.scenarios.support.data_triggers import DataTriggers


class MapRevealer:

    def __init__(self, scenario: AoE2DEScenario):
        self.trigger_manager: TriggerManager = scenario.trigger_manager
        self.map_manager = scenario.map_manager
        create_revealers = self.trigger_manager.add_trigger("Create Revealers")
        for x in range(0, scenario.map_manager.map_width, 20):
            for y in range(0, scenario.map_manager.map_height, 20):
                for player in [PlayerId.ONE, PlayerId.TWO, PlayerId.THREE, PlayerId.FOUR, PlayerId.FIVE,
                               PlayerId.SIX, PlayerId.SEVEN]:
                    create_revealers.new_effect.create_object(
                        object_list_unit_id=OtherInfo.MAP_REVEALER_GIANT.ID,
                        location_x=x,
                        location_y=y,
                        source_player=player
                    )
        map_area = scenario.new.area().select_entire_map()
        remove_revealers = self.trigger_manager.add_trigger("Remove Revealers")
        remove_revealers.new_condition.timer(timer=2)
        for player in [PlayerId.ONE, PlayerId.TWO, PlayerId.THREE, PlayerId.FOUR, PlayerId.FIVE,
                       PlayerId.SIX, PlayerId.SEVEN]:
            remove_revealers.new_effect.remove_object(
                object_list_unit_id=OtherInfo.MAP_REVEALER_GIANT.ID,
                area_x1=map_area.x1,
                area_y1=map_area.y1,
                area_x2=map_area.x2,
                area_y2=map_area.y2,
                source_player=player
            )






