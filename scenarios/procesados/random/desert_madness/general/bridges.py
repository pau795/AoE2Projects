from AoE2ScenarioParser.datasets.buildings import BuildingInfo
from AoE2ScenarioParser.datasets.players import PlayerId
from AoE2ScenarioParser.datasets.terrains import TerrainId
from AoE2ScenarioParser.datasets.trigger_lists import ObjectAttribute, Operation
from AoE2ScenarioParser.objects.managers.trigger_manager import TriggerManager
from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario
from AoE2ScenarioParser.scenarios.support.data_triggers import DataTriggers


class Bridges:

    def __init__(self, scenario: AoE2DEScenario, trigger_data: DataTriggers):
        self.trigger_manager: TriggerManager = scenario.trigger_manager
        self.trigger_data = trigger_data
        self.bridges = self.trigger_data.tiles['bridge']
        self.bridge()

    def bridge(self):
        bridge = self.trigger_manager.add_trigger("Bridge")

        bridge.new_effect.modify_attribute(
            object_list_unit_id=BuildingInfo.BRIDGE_A_MIDDLE.ID,
            source_player=PlayerId.GAIA,
            object_attributes=ObjectAttribute.FOUNDATION_TERRAIN,
            operation=Operation.SET,
            quantity=TerrainId.BLACK
        )

        bridge.new_effect.modify_attribute(
            object_list_unit_id=BuildingInfo.BRIDGE_B_MIDDLE.ID,
            source_player=PlayerId.GAIA,
            object_attributes=ObjectAttribute.FOUNDATION_TERRAIN,
            operation=Operation.SET,
            quantity=TerrainId.BLACK
        )

        bridge.new_effect.create_object(
            object_list_unit_id=BuildingInfo.BRIDGE_A_MIDDLE.ID,
            location_x=self.bridges[0].x,
            location_y=self.bridges[0].y,
            source_player=PlayerId.GAIA
        )

        bridge.new_effect.create_object(
            object_list_unit_id=BuildingInfo.BRIDGE_A_MIDDLE.ID,
            location_x=self.bridges[1].x,
            location_y=self.bridges[1].y,
            source_player=PlayerId.GAIA
        )

        bridge.new_effect.create_object(
            object_list_unit_id=BuildingInfo.BRIDGE_A_MIDDLE.ID,
            location_x=self.bridges[2].x,
            location_y=self.bridges[2].y,
            source_player=PlayerId.GAIA
        )

        bridge.new_effect.create_object(
            object_list_unit_id=BuildingInfo.BRIDGE_B_MIDDLE.ID,
            location_x=self.bridges[3].x,
            location_y=self.bridges[3].y,
            source_player=PlayerId.GAIA
        )

        bridge.new_effect.create_object(
            object_list_unit_id=BuildingInfo.BRIDGE_B_MIDDLE.ID,
            location_x=self.bridges[4].x,
            location_y=self.bridges[4].y,
            source_player=PlayerId.GAIA
        )

        for b in self.bridges:
            bridge.new_effect.remove_object(
                source_player=PlayerId.GAIA,
                area_x1=b.x,
                area_y1=b.y,
                area_x2=b.x,
                area_y2=b.y,
            )
