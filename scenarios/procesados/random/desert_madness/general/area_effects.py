from AoE2ScenarioParser.datasets.players import PlayerId
from AoE2ScenarioParser.objects.managers.trigger_manager import TriggerManager
from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario
from AoE2ScenarioParser.scenarios.support.data_triggers import DataTriggers


class AreaEffects:

    def __init__(self, scenario: AoE2DEScenario, trigger_data: DataTriggers):
        self.trigger_manager: TriggerManager = scenario.trigger_manager
        self.trigger_data = trigger_data
        self.darkness_areas = self.trigger_data.areas['darkness']
        self.healing_well = self.trigger_data.areas['healing_well']
        self.area_effects()

    def area_effects(self):
        darkness = self.trigger_manager.add_trigger("Darkness", looping=True)
        for area in self.darkness_areas:
            for player in [PlayerId.ONE, PlayerId.TWO, PlayerId.THREE, PlayerId.FOUR, PlayerId.FIVE, PlayerId.SIX,
                           PlayerId.SEVEN, PlayerId.EIGHT, PlayerId.GAIA]:
                darkness.new_effect.kill_object(
                    source_player=player,
                    area_x1=area.x1,
                    area_y1=area.y1,
                    area_x2=area.x2,
                    area_y2=area.y2
                )

        healing_well = self.trigger_manager.add_trigger("Healing Well", looping=True)
        for area in self.healing_well:
            for player in [PlayerId.ONE, PlayerId.TWO, PlayerId.THREE, PlayerId.FOUR, PlayerId.FIVE, PlayerId.SIX,
                           PlayerId.SEVEN]:
                healing_well.new_effect.heal_object(
                    source_player=player,
                    area_x1=area.x1,
                    area_y1=area.y1,
                    area_x2=area.x2,
                    area_y2=area.y2,
                    quantity=3
                )


