from AoE2ScenarioParser.datasets.other import OtherInfo
from AoE2ScenarioParser.datasets.players import PlayerId
from AoE2ScenarioParser.datasets.trigger_lists import ObjectAttribute, Operation, AttackStance, FogVisibility
from AoE2ScenarioParser.datasets.units import UnitInfo
from AoE2ScenarioParser.objects.managers.trigger_manager import TriggerManager
from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario
from AoE2ScenarioParser.scenarios.support.data_triggers import DataTriggers


class BarrelPetards:

    def __init__(self, scenario: AoE2DEScenario, trigger_data: DataTriggers):
        self.trigger_manager: TriggerManager = scenario.trigger_manager
        self.map_manager = scenario.map_manager
        self.barrel_petards_areas = trigger_data.areas['barrel_petards']
        self.petard_attributes()
        self.barrel_petards()

    def petard_attributes(self):
        petard_attributes = self.trigger_manager.add_trigger("Petard Attributes")
        petard_attributes.new_effect.modify_attribute(
            object_list_unit_id=UnitInfo.PETARD.ID,
            source_player=PlayerId.EIGHT,
            object_attributes=ObjectAttribute.UNIT_SIZE_Z,
            operation=Operation.SET,
            quantity=0
        )
        petard_attributes.new_effect.modify_attribute(
            object_list_unit_id=UnitInfo.PETARD.ID,
            source_player=PlayerId.EIGHT,
            object_attributes=ObjectAttribute.MAX_RANGE,
            operation=Operation.SET,
            quantity=30
        )
        petard_attributes.new_effect.modify_attribute(
            object_list_unit_id=UnitInfo.PETARD.ID,
            source_player=PlayerId.EIGHT,
            object_attributes=ObjectAttribute.MAX_RANGE,
            operation=Operation.DIVIDE,
            quantity=100
        )
        petard_attributes.new_effect.modify_attribute(
            object_list_unit_id=UnitInfo.PETARD.ID,
            source_player=PlayerId.EIGHT,
            object_attributes=ObjectAttribute.BLAST_WIDTH,
            operation=Operation.SET,
            quantity=75
        )
        petard_attributes.new_effect.modify_attribute(
            object_list_unit_id=UnitInfo.PETARD.ID,
            source_player=PlayerId.EIGHT,
            object_attributes=ObjectAttribute.BLAST_WIDTH,
            operation=Operation.DIVIDE,
            quantity=100
        )
        petard_attributes.new_effect.modify_attribute(
            object_list_unit_id=UnitInfo.PETARD.ID,
            source_player=PlayerId.EIGHT,
            object_attributes=ObjectAttribute.STANDING_GRAPHIC,
            operation=Operation.SET,
            quantity=8346
        )
        petard_attributes.new_effect.modify_attribute(
            object_list_unit_id=UnitInfo.PETARD.ID,
            source_player=PlayerId.EIGHT,
            object_attributes=ObjectAttribute.DYING_GRAPHIC,
            operation=Operation.SET,
            quantity=3933
        )
        petard_attributes.new_effect.modify_attribute(
            object_list_unit_id=UnitInfo.PETARD.ID,
            source_player=PlayerId.EIGHT,
            object_attributes=ObjectAttribute.ICON_ID,
            operation=Operation.SET,
            quantity=57
        )
        petard_attributes.new_effect.modify_attribute(
            object_list_unit_id=UnitInfo.PETARD.ID,
            source_player=PlayerId.EIGHT,
            object_attributes=ObjectAttribute.FOG_VISIBILITY,
            operation=Operation.SET,
            quantity=FogVisibility.ALWAYS_VISIBLE
        )

        petard_attributes.new_effect.modify_attribute(
            object_list_unit_id=UnitInfo.PETARD.ID,
            source_player=PlayerId.EIGHT,
            object_attributes=ObjectAttribute.OBJECT_NAME_ID,
            operation=Operation.SET,
            quantity=5305
        )

        self.trigger_manager.copy_trigger_per_player(
            trigger_select=petard_attributes.trigger_id,
            from_player=PlayerId.EIGHT,
            create_copy_for_players=[PlayerId.ONE, PlayerId.TWO, PlayerId.THREE,
                                     PlayerId.FOUR, PlayerId.FIVE, PlayerId.SIX, PlayerId.SEVEN]
        )

    def barrel_petards(self):
        barrel_reset = self.trigger_manager.add_trigger("Barrel Reset", looping=True)
        barrel_reset.new_condition.timer(timer=60)
        i = 0
        for area in self.barrel_petards_areas:
            barrel_reset.new_effect.remove_object(
                object_list_unit_id=UnitInfo.PETARD.ID,
                source_player=PlayerId.EIGHT,
                area_x1=area.x1,
                area_y1=area.y1,
                area_x2=area.x2,
                area_y2=area.y2
            )
            barrel_reset.new_effect.remove_object(
                object_list_unit_id=OtherInfo.BARRELS.ID,
                source_player=PlayerId.GAIA,
                area_x1=area.x1,
                area_y1=area.y1,
                area_x2=area.x2,
                area_y2=area.y2
            )

            for tile in area.to_coords():
                if (tile.x + tile.y) % 2 == 0:
                    create_petards = self.trigger_manager.add_trigger(f'Create Petards {i}')
                    create_barrels = self.trigger_manager.add_trigger(f'Create Barrels {i}')
                    create_petards.new_condition.chance(quantity=50)
                    barrel_reset.new_effect.activate_trigger(create_petards.trigger_id)
                    barrel_reset.new_effect.activate_trigger(create_barrels.trigger_id)
                    create_petards.new_effect.create_object(
                        object_list_unit_id=UnitInfo.PETARD.ID,
                        source_player=PlayerId.EIGHT,
                        location_x=tile.x,
                        location_y=tile.y,
                    )

                    create_petards.new_effect.change_object_stance(
                        object_list_unit_id=UnitInfo.PETARD.ID,
                        source_player=PlayerId.EIGHT,
                        area_x1=tile.x,
                        area_y1=tile.y,
                        area_x2=tile.x,
                        area_y2=tile.y,
                        attack_stance=AttackStance.STAND_GROUND
                    )

                    create_petards.new_effect.deactivate_trigger(create_barrels.trigger_id)
                    create_barrels.new_effect.create_object(
                        object_list_unit_id=OtherInfo.BARRELS.ID,
                        source_player=PlayerId.GAIA,
                        location_x=tile.x,
                        location_y=tile.y,
                    )
                    create_barrels.new_effect.deactivate_trigger(create_petards.trigger_id)
                    i += 1
