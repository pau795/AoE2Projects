from AoE2ScenarioParser.datasets.players import PlayerId
from AoE2ScenarioParser.datasets.trigger_lists import ObjectAttribute, Operation, ObjectState, Comparison, Attribute, ActionType
from AoE2ScenarioParser.datasets.units import UnitInfo
from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario
from AoE2ScenarioParser.scenarios.support.data_triggers import DataTriggers

from scenarios.procesados.clash_royale.cr_constants import ClashRoyaleVariables, ClashRoyaleSounds
from scenarios.procesados.clash_royale.cr_helper import ClashRoyaleBridges


class ClashRoyaleUnitFactory:

    def __init__(self, scenario: AoE2DEScenario, data_triggers: DataTriggers) -> None:
        self.scenario = scenario
        self.trigger_manager = scenario.trigger_manager
        self.data_triggers = data_triggers
        self.player_list = [PlayerId.ONE, PlayerId.TWO]
        self.arena_area = self.data_triggers.areas["arena"][0]

    def setup_bridges(self):
        selection_dict = {
            PlayerId.ONE: (ClashRoyaleVariables.DECK_SELECT_PLAYER1.ID, ClashRoyaleVariables.HOTKEY_SELECT_PLAYER1),
            PlayerId.TWO: (ClashRoyaleVariables.DECK_SELECT_PLAYER2.ID, ClashRoyaleVariables.HOTKEY_SELECT_PLAYER2),
        }
        loop_dict = {
            PlayerId.ONE: PlayerId.THREE,
            PlayerId.TWO: PlayerId.FOUR,
        }
        for (cr_unit, bridge_object) in ClashRoyaleBridges.BRIDGES.items():
            bridge_id = bridge_object["bridge"]
            for player, select_variable, hotkey_variable in selection_dict.items():
                selection_zone = self.data_triggers.areas[f"DS_{cr_unit.lower()}_p{player}"]
                deck_select_trigger = self.trigger_manager.add_trigger(f"Deck Select {cr_unit.lower()} P{player}")
                deck_select_trigger.new_condition.objects_in_area(
                    object_list=UnitInfo.KING.ID,
                    source_player=player,
                    quantity=1,
                    object_state=ObjectState.ALIVE,
                    area_x1=selection_zone[0].x1,
                    area_y1=selection_zone[0].y1,
                    area_x2=selection_zone[0].x2,
                    area_y2=selection_zone[0].y2
                )
                deck_select_trigger.new_condition.variable_value(
                    variable=select_variable,
                    quantity=8,
                    comparison=Comparison.LESS,
                ),
                deck_select_trigger.new_effect.modify_attribute_by_variable(
                    source_player=player,
                    object_list_unit_id=bridge_id,
                    object_attributes=ObjectAttribute.TRAIN_BUTTON,
                    operation=Operation.SET,
                    variable=select_variable,
                ),
                deck_select_trigger.new_effect.modify_attribute_by_variable(
                    source_player=player,
                    object_list_unit_id=bridge_id,
                    object_attributes=ObjectAttribute.HOTKEY_ID,
                    operation=Operation.SET,
                    variable=hotkey_variable,
                )
                deck_select_trigger.new_effect.change_variable(
                    variable=select_variable,
                    operation=Operation.ADD,
                    quantity=1,
                )
                deck_select_trigger.new_effect.remove_object(
                    source_player=player,
                    area_x1=selection_zone[1].x1,
                    area_y1=selection_zone[1].y1,
                    area_x2=selection_zone[1].x2,
                    area_y2=selection_zone[1].y2,
                )
                deck_select_trigger.new_effect.play_sound(
                    source_player=player,
                    sound_name=ClashRoyaleSounds.CARD_SELECT,
                    location_x=int(selection_zone[0].get_center()[0]),
                    location_y=int(selection_zone[0].get_center()[1]),
                )
                bridge_object["selection_trigger"] = deck_select_trigger
            for player, replace_player in loop_dict.items():
                card_rotation_trigger = self.trigger_manager.add_trigger(f"Card Rotation {cr_unit.lower()} P{player}", enabled=False)
                card_rotation_trigger.new_condition.variable_value(
                    variable=bridge_object["variable"][player].ID,
                    comparison=Comparison.LESS_OR_EQUAL,
                    quantity=0
                )
                card_rotation_trigger.new_effect.enable_disable_object(
                    object_list_unit_id=bridge_id,
                    source_player=player,
                    enabled=True
                )

                bridge_loop_trigger = self.trigger_manager.add_trigger(f"Bridge Loop {bridge_id} p{player}", enabled=False, looping=True)
                bridge_loop_trigger.new_condition.objects_in_area(
                    object_list=bridge_object["bridge"],
                    area_x1=self.arena_area.x1,
                    area_y1=self.arena_area.y1,
                    area_x2=self.arena_area.x2,
                    area_y2=self.arena_area.y2,
                    object_state=ObjectState.ALIVE,
                    quantity=1
                )
                if bridge_object["direct"]:
                    if len(bridge_object["units"]) == 1:
                        for replace_unit, quantity in bridge_object["units"].items():
                            if quantity == 1:
                                bridge_loop_trigger.new_effect.replace_object(
                                    source_player=player,
                                    object_list_unit_id=bridge_id,
                                    object_list_unit_id_2=replace_unit,
                                    target_player=replace_player,
                                    area_x1=self.arena_area.x1,
                                    area_y1=self.arena_area.y1,
                                    area_x2=self.arena_area.x2,
                                    area_y2=self.arena_area.y2,
                                )
                                if "delete_delay" in bridge_object:
                                    delete_delay_trigger = self.trigger_manager.add_trigger(f"Delete Delay {bridge_id} p{player}", enabled=False)
                                    delete_delay_trigger.new_condition.timer(
                                        timer=bridge_object["delete_delay"]
                                    )
                                    delete_delay_trigger.new_effect.remove_object(
                                        object_list_unit_id=replace_unit,
                                        source_player=replace_player,
                                        area_x1=self.arena_area.x1,
                                        area_y1=self.arena_area.y1,
                                        area_x2=self.arena_area.x2,
                                        area_y2=self.arena_area.y2,
                                        object_state=ObjectState.ALIVE,
                                    )
                                    bridge_loop_trigger.new_effect.activate_trigger(
                                        trigger_id=delete_delay_trigger.trigger_id
                                    )
                            else:
                                print(f"Bridge {cr_unit} dict is direct but replacement not have {quantity} units")
                    else:
                        print(f"Bridge {cr_unit} dict is direct but has more than 1 replacement units")
                else:
                    first = True
                    first_unit = None
                    for replace_unit, quantity in bridge_object["units"].items():
                        for i in range(quantity):
                            if first:
                                first_unit = replace_unit
                                bridge_loop_trigger.new_effect.replace_object(
                                    object_list_unit_id=bridge_id,
                                    object_list_unit_id_2=replace_unit,
                                    source_player=player,
                                    target_player=replace_player,
                                    area_x1=self.arena_area.x1,
                                    area_y1=self.arena_area.y1,
                                    area_x2=self.arena_area.x2,
                                    area_y2=self.arena_area.y2
                                )
                                first = False
                            else:
                                bridge_loop_trigger.new_effect.create_garrisoned_object(
                                    object_list_unit_id=first_unit,
                                    object_list_unit_id_2=replace_unit,
                                    source_player=player,
                                    area_x1=self.arena_area.x1,
                                    area_y1=self.arena_area.y1,
                                    area_x2=self.arena_area.x2,
                                    area_y2=self.arena_area.y2
                                )
                        bridge_loop_trigger.new_effect.change_ownership(
                            object_list_unit_id=replace_unit,
                            source_player=player,
                            target_player=replace_player,
                            area_x1=self.arena_area.x1,
                            area_y1=self.arena_area.y1,
                            area_x2=self.arena_area.x2,
                            area_y2=self.arena_area.y2
                        )
                        bridge_loop_trigger.new_effect.task_object(
                            object_list_unit_id=replace_unit,
                            source_player=replace_player,
                            area_x1=self.arena_area.x1,
                            area_y1=self.arena_area.y1,
                            area_x2=self.arena_area.x2,
                            area_y2=self.arena_area.y2,
                            action_type=ActionType.UNGARRISON,
                        )
                for sound_player in loop_dict.keys():
                    bridge_loop_trigger.new_effect.play_sound(
                        source_player=sound_player,
                        sound_name=bridge_object["sound"],
                        location_x=int(self.arena_area.get_center()[0]),
                        location_y=int(self.arena_area.get_center()[1])
                    )
                bridge_loop_trigger.new_effect.enable_disable_object(
                    object_list_unit_id=bridge_id,
                    source_player=player,
                    enabled=False,
                )
                bridge_loop_trigger.new_effect.change_variable(
                    variable=bridge_object["variable"][player].ID,
                    operation=Operation.SET,
                    quantity=5
                )
                bridge_loop_trigger.new_effect.modify_resource(
                    source_player=player,
                    tribute_list=Attribute.WOOD_STORAGE,
                    operation=Operation.SET,
                    quantity=1
                )
                bridge_loop_trigger.new_effect.activate_trigger(
                    trigger_id=card_rotation_trigger.trigger_id
                )
