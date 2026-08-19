from AoE2ScenarioParser.datasets.other import OtherInfo
from AoE2ScenarioParser.datasets.players import PlayerId
from AoE2ScenarioParser.datasets.trigger_lists import Comparison, Operation, PanelLocation
from AoE2ScenarioParser.datasets.units import UnitInfo
from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario
from AoE2ScenarioParser.scenarios.support.data_triggers import DataTriggers

from scenarios.procesados.clash_royale.cr_constants import ClashRoyaleVariables, ClashRoyaleHotkeys, ClashRoyaleSounds, ClashRoyaleStrings


class ClashRoyaleStart:

    def __init__(self, scenario: AoE2DEScenario, data_triggers: DataTriggers):
        self.scenario = scenario
        self.data_triggers = data_triggers
        self.trigger_manager = self.scenario.trigger_manager
        self.player_manager = self.scenario.player_manager
        self.message_manager = self.scenario.message_manager
        self.human_player_list = [PlayerId.ONE, PlayerId.TWO]
        self.ready_area_p1 = self.data_triggers.areas["ready_area_p1"][0]
        self.ready_area_p2 = self.data_triggers.areas["ready_area_p2"][0]
        self.villager_position_p1 = self.data_triggers.tiles["villager_p1"][0]
        self.villager_position_p2 = self.data_triggers.tiles["villager_p2"][0]
        self.trigger_manager.add_variable(ClashRoyaleVariables.DECK_SELECT_PLAYER1.NAME, ClashRoyaleVariables.DECK_SELECT_PLAYER1.ID)
        self.trigger_manager.add_variable(ClashRoyaleVariables.DECK_SELECT_PLAYER2.NAME, ClashRoyaleVariables.DECK_SELECT_PLAYER2.ID)
        self.trigger_manager.add_variable(ClashRoyaleVariables.HOTKEY_SELECT_PLAYER1.NAME, ClashRoyaleVariables.HOTKEY_SELECT_PLAYER1.ID)
        self.trigger_manager.add_variable(ClashRoyaleVariables.HOTKEY_SELECT_PLAYER2.NAME, ClashRoyaleVariables.HOTKEY_SELECT_PLAYER2.ID)
        self.player_manager.players[PlayerId.THREE].string_table_name_id = ClashRoyaleStrings.PLAYER1
        self.player_manager.players[PlayerId.FOUR].string_table_name_id = ClashRoyaleStrings.PLAYER2
        self.player_manager.players[PlayerId.FIVE].string_table_name_id = ClashRoyaleStrings.PLAYER_ARENA
        self.message_manager.instructions_string_table_id = ClashRoyaleStrings.SCENARIO_INSTRUCTIONS
        self.message_manager.hints_string_table_id = ClashRoyaleStrings.SCENARIO_HINTS

        for i, hotkey_id in ClashRoyaleHotkeys.HOTKEY_DICT.items():
            for player in self.human_player_list:
                ds_variable_id = ClashRoyaleVariables.DECK_SELECT_PLAYER1 if player == PlayerId.ONE else ClashRoyaleVariables.DECK_SELECT_PLAYER2
                hotkey_variable_id = ClashRoyaleVariables.HOTKEY_SELECT_PLAYER1 if player == PlayerId.ONE else ClashRoyaleVariables.HOTKEY_SELECT_PLAYER2

                ds_hotkey = self.trigger_manager.add_trigger(f"Deck Select Hotkey{hotkey_id} P{player}")
                ds_hotkey.new_condition.variable_value(
                    variable=ds_variable_id.ID,
                    comparison=Comparison.EQUAL,
                    quantity=i
                )
                ds_hotkey.new_effect.change_variable(
                    variable=hotkey_variable_id.ID,
                    operation=Operation.SET,
                    quantity=hotkey_id
                )

        deck_select_finished_dict = {
            PlayerId.ONE: (ClashRoyaleStrings.SELECT_FINISHED_P1, self.ready_area_p1, PanelLocation.TOP),
            PlayerId.TWO: (ClashRoyaleStrings.SELECT_FINISHED_P2, self.ready_area_p2, PanelLocation.BOTTOM)
        }

        for player, string_id, player_area, panel_location in deck_select_finished_dict.items():
            selection_finished = self.trigger_manager.add_trigger(f"Deck Select Finished P{player}")
            selection_finished.new_condition.variable_value(
                variable=ClashRoyaleVariables.DECK_SELECT_PLAYER1.ID,
                comparison=Comparison.EQUAL,
                quantity=8
            )
            selection_finished.new_effect.display_instructions(
                object_list_unit_id=UnitInfo.KING.ID,
                source_player=player,
                string_id=string_id,
                sound_name=ClashRoyaleSounds.PLAYER_WAITING,
                instruction_panel_position=panel_location
            )
            selection_finished.new_effect.remove_object(
                object_list_unit_id=OtherInfo.ROCK_FORMATION_1.ID,
                area_x1=player_area.x1,
                area_y1=player_area.y1,
                area_x2=player_area.x2,
                area_y2=player_area.y2,
            )
            selection_finished.new_effect.change_view(
                location_x=int(player_area.get_center()[0]),
                location_y=int(player_area.get_center()[1]),
                scroll=True
            )

        # ------------------------------------------
        #           MATCH STARTS TRIGGERS
        # -------------------------------------------

        players_ready = self.trigger_manager.add_trigger(f"Players ready")
        match_starts = self.trigger_manager.add_trigger(f"Match Starts", enabled=False)
        players_ready.new_condition.objects_in_area(
            object_list=UnitInfo.KING.ID,
            source_player=PlayerId.ONE,
            area_x1=self.ready_area_p1.x1,
            area_y1=self.ready_area_p1.y1,
            area_x2=self.ready_area_p1.x2,
            area_y2=self.ready_area_p1.y2
        )
        players_ready.new_condition.objects_in_area(
            object_list=UnitInfo.KING.ID,
            source_player=PlayerId.TWO,
            area_x1=self.ready_area_p1.x1,
            area_y1=self.ready_area_p1.y1,
            area_x2=self.ready_area_p1.x2,
            area_y2=self.ready_area_p1.y2
        )
        players_ready.new_effect.display_instructions(
            source_player=PlayerId.GAIA,
            string_id=ClashRoyaleStrings.MATCH_STARTS_WARNING,
            sound_name=ClashRoyaleSounds.PLAYER_WAITING,
            instruction_panel_position=PanelLocation.MIDDLE
        )
        players_ready.new_effect.change_view(
            source_player=PlayerId.ONE,
            location_x=self.villager_position_p1.x,
            location_y=self.villager_position_p1.y,
            scroll=True
        )
        players_ready.new_effect.change_view(
            source_player=PlayerId.TWO,
            location_x=self.villager_position_p2.x,
            location_y=self.villager_position_p2.y,
            scroll=True
        )
        players_ready.new_effect.activate_trigger(match_starts.trigger_id)

        match_starts.new_effect.create_object(
            object_list_unit_id=UnitInfo.VILLAGER_MALE.ID,
            source_player=PlayerId.ONE,
            location_x=self.villager_position_p1.x,
            location_y=self.villager_position_p1.y
        )

        match_starts.new_effect.create_object(
            object_list_unit_id=UnitInfo.VILLAGER_MALE.ID,
            source_player=PlayerId.TWO,
            location_x=self.villager_position_p2.x,
            location_y=self.villager_position_p2.y
        )
