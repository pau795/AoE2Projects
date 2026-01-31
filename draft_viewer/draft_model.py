from dataclasses import dataclass
from enum import Enum


class PlayerType(Enum):
    HOST = 'HOST'
    GUEST = 'GUEST'
    NONE = 'NONE'
    SPEC = 'SPEC'


class ActionType(Enum):
    PICK = 'PICK'
    BAN = 'BAN'
    SNIPE = 'SNIPE'
    STEAL = 'STEAL'
    REVEAL_ALL = 'REVEAL_ALL'
    REVEAL_PICKS = 'REVEAL_PICKS'
    REVEAL_BANS = 'REVEAL_BANS'
    REVEAL_SNIPES = 'REVEAL_SNIPES'
    PAUSE = 'PAUSE'
    RESET_CL = 'RESET_CL'


@dataclass
class Turn:
    player: PlayerType
    action: ActionType
    chosen_option: str | None
    is_random: bool | None
    sniped: bool

    @staticmethod
    def from_dict(data: dict):
        return Turn(
            player=PlayerType(data['player'].upper()),
            action=ActionType(data['actionType'].upper()) if 'actionType' in data else ActionType(data['action'].upper()) if 'action' in data else None,
            chosen_option=data['chosenOptionId'] if 'chosenOptionId' in data else None,
            is_random=data['isRandomlyChosen'] == "true" if 'isRandomlyChosen' in data else None,
            sniped=False
        )


@dataclass
class DraftModel:
    host_name: str
    guest_name: str
    preset_id: str
    host_picks: list[Turn]
    host_bans: list[Turn]
    guest_picks: list[Turn]
    guest_bans: list[Turn]
    admin_picks: list[Turn]
    admin_bans: list[Turn]

    @staticmethod
    def from_dict(data: dict):
        turns = [Turn.from_dict(turn) for turn in data['events']]
        draft = DraftModel(
            host_name=data['nameHost'],
            guest_name=data['nameGuest'],
            preset_id=data['preset']['presetId'],
            host_picks=[turn for turn in turns if turn.player == PlayerType.HOST and turn.action == ActionType.PICK],
            host_bans=[turn for turn in turns if turn.player == PlayerType.HOST and turn.action == ActionType.BAN],
            guest_picks=[turn for turn in turns if turn.player == PlayerType.GUEST and turn.action == ActionType.PICK],
            guest_bans=[turn for turn in turns if turn.player == PlayerType.GUEST and turn.action == ActionType.BAN],
            admin_picks=[turn for turn in turns if turn.player == PlayerType.NONE and turn.action == ActionType.PICK],
            admin_bans=[turn for turn in turns if turn.player == PlayerType.NONE and turn.action == ActionType.BAN],

        )
        for snipe_turn in turns:
            if snipe_turn.action == ActionType.SNIPE:
                player_picks = draft.guest_picks if snipe_turn.player == PlayerType.HOST else draft.host_picks if snipe_turn.player == PlayerType.GUEST else None
                if player_picks:
                    for player_turn in player_picks:
                        if player_turn.chosen_option == snipe_turn.chosen_option:
                            player_turn.sniped = True

        return draft

    def set_admin_civilizations(self, selected_round: str):
        banned_civs = []
        civs = ["huns", "mongols", "gurjaras", "khmer"]
        for civ in civs:
            banned_civs.append(Turn(
                player=PlayerType.NONE,
                action=ActionType.BAN,
                chosen_option=civ,
                is_random=False,
                sniped=False
            ))
        self.admin_bans = banned_civs + self.admin_bans

    def set_admin_maps(self, selected_round: str):
        admin_picks = []
        admin_bans = []

        selected_maps = []
        banned_maps = []
        match selected_round:
            case "round_1":
                selected_maps.append("earthquake")
                banned_maps.extend(["fukushima", "the_plague"])
            case "round_2":
                selected_maps.append("fukushima")
                banned_maps.extend(["earthquake", "the_plague"])
            case "round_3":
                selected_maps.append("the_plague")
                banned_maps.extend(["earthquake", "fukushima"])
            case "3rd/4th":
                selected_maps.extend(["alcatraz", "armaggedon"])
                banned_maps.extend(["twister"])
            case "finals":
                selected_maps.append("vulcan nomad")
                banned_maps.extend(["twister"])

        for map1 in selected_maps:
            admin_picks.append(Turn(
                player=PlayerType.NONE,
                action=ActionType.PICK,
                chosen_option=map1,
                is_random=False,
                sniped=False
            ))
        for map2 in banned_maps:
            admin_bans.append(Turn(
                player=PlayerType.NONE,
                action=ActionType.BAN,
                chosen_option=map2,
                is_random=False,
                sniped=False
            ))
        self.admin_picks = admin_picks + self.admin_picks
        self.admin_bans = admin_bans + self.admin_bans

