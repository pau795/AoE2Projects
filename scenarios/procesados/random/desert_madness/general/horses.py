from AoE2ScenarioParser.datasets.players import PlayerId
from AoE2ScenarioParser.datasets.trigger_lists import ObjectAttribute, Operation, FogVisibility
from AoE2ScenarioParser.datasets.units import UnitInfo
from AoE2ScenarioParser.objects.managers.trigger_manager import TriggerManager
from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario
from AoE2ScenarioParser.scenarios.support.data_triggers import DataTriggers


class Horses:

    def __init__(self, scenario: AoE2DEScenario, trigger_data: DataTriggers):
        self.trigger_manager: TriggerManager = scenario.trigger_manager
        self.trigger_data = trigger_data
        self.horse_tiles = self.trigger_data.tiles['horses']
        self.horses()

    def horses(self):
        init_horses = self.trigger_manager.add_trigger("Init Horses")
        for player in [PlayerId.ONE, PlayerId.TWO, PlayerId.THREE, PlayerId.FOUR, PlayerId.FIVE,
                       PlayerId.SIX, PlayerId.SEVEN, PlayerId.EIGHT, PlayerId.GAIA]:
            init_horses.new_effect.modify_attribute(
                object_list_unit_id=UnitInfo.HORSE_A.ID,
                source_player=player,
                object_attributes=ObjectAttribute.LINE_OF_SIGHT,
                operation=Operation.SET,
                quantity=1
            )
            init_horses.new_effect.modify_attribute(
                object_list_unit_id=UnitInfo.HORSE_A.ID,
                source_player=player,
                object_attributes=ObjectAttribute.STANDING_GRAPHIC,
                operation=Operation.SET,
                quantity=0
            )

        create_horses = self.trigger_manager.add_trigger('Create Horses')
        create_horses.new_condition.timer(timer=2)
        for tile in self.horse_tiles:
            create_horses.new_effect.create_object(
                object_list_unit_id=UnitInfo.HORSE_A.ID,
                location_x=tile.x,
                location_y=tile.y,
                source_player=PlayerId.GAIA
            )

        for player, tile in zip([PlayerId.ONE, PlayerId.TWO, PlayerId.THREE,
                                 PlayerId.FOUR, PlayerId.FIVE, PlayerId.SIX, PlayerId.SEVEN], self.horse_tiles):
            horse_check = self.trigger_manager.add_trigger(f'Horse Check P{player}')
            horse_check.new_condition.timer(timer=3)
            horse_check.new_condition.objects_in_area(
                object_list=UnitInfo.HORSE_A.ID,
                area_x1=tile.x,
                area_y1=tile.y,
                area_x2=tile.x,
                area_y2=tile.y,
                source_player=PlayerId.GAIA,
                quantity=1
            )
            horse_check.new_effect.declare_victory(
                source_player=player,
                enabled=False
            )

        finish_horses = self.trigger_manager.add_trigger('Finish Horses')
        finish_horses.new_condition.timer(timer=4)
        for player in [PlayerId.ONE, PlayerId.TWO, PlayerId.THREE, PlayerId.FOUR, PlayerId.FIVE,
                       PlayerId.SIX, PlayerId.SEVEN, PlayerId.EIGHT, PlayerId.GAIA]:
            finish_horses.new_effect.modify_attribute(
                object_list_unit_id=UnitInfo.HORSE_A.ID,
                source_player=player,
                object_attributes=ObjectAttribute.LINE_OF_SIGHT,
                operation=Operation.SET,
                quantity=0
            )
            finish_horses.new_effect.modify_attribute(
                object_list_unit_id=UnitInfo.HORSE_A.ID,
                source_player=player,
                object_attributes=ObjectAttribute.FOG_VISIBILITY,
                operation=Operation.SET,
                quantity=FogVisibility.NOT_VISIBLE
            )

        for player, tile in zip([PlayerId.ONE, PlayerId.TWO, PlayerId.THREE,
                                 PlayerId.FOUR, PlayerId.FIVE, PlayerId.SIX, PlayerId.SEVEN], self.horse_tiles):

            finish_horses.new_effect.remove_object(
                object_list_unit_id=UnitInfo.HORSE_A.ID,
                area_x1=tile.x,
                area_y1=tile.y,
                area_x2=tile.x,
                area_y2=tile.y,
                source_player=player
            )
            finish_horses.new_effect.remove_object(
                object_list_unit_id=UnitInfo.HORSE_A.ID,
                area_x1=tile.x,
                area_y1=tile.y,
                area_x2=tile.x,
                area_y2=tile.y,
                source_player=PlayerId.GAIA
            )




