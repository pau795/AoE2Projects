from datetime import datetime, timezone
from dataclasses import dataclass
import gspread
from google.oauth2.service_account import Credentials
import requests

clan_1v1_url = "https://data.aoe2companion.com/api/leaderboards/rm_1v1?clan=DYNB"
clan_tg_url = "https://data.aoe2companion.com/api/leaderboards/rm_team?clan=DYNB"
api_headers = {
    "User-Agent": "Mozilla/5.0"
}

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_file(
    "aoe2dynamic-credentials.json",
    scopes=SCOPES
)


@dataclass
class Leaderboard:
    type: str
    name: str
    elo: int
    max_elo: int
    total_games: int
    wins: int
    winrate: float
    last_match: str


@dataclass
class Member:
    id: int
    name: str
    avatar_url: str
    total_games: int
    flag: str
    leaderboard: dict[str, Leaderboard]


def get_leaderboard_data(member_list: list[Member], leaderboard_data) -> list[Member]:
    for player in leaderboard_data['players']:
        leaderboard = Leaderboard(
            type=player['leaderboardId'],
            name=player['name'],
            elo=player['rating'],
            max_elo=player['maxRating'],
            total_games=player['games'],
            wins=player['wins'],
            winrate=0,
            last_match=player['lastMatchTime']
        )
        leaderboard.winrate = float(leaderboard.wins / leaderboard.total_games)

        for member in member_list:
            if member.name == leaderboard.name:
                member.leaderboard[leaderboard.type] = leaderboard
                break
    return member_list


def country_code_to_flag(code):
    code = code.upper()
    return ''.join(chr(127397 + ord(c)) for c in code)


def date_transform(date_str: str) -> str:
    dt = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
    dt = dt.astimezone(timezone.utc)

    return dt.strftime("%Y-%m-%d %H:%M:%S UTC")


def get_members() -> list[Member]:
    members = []
    clan_members_page = 1
    while True:
        clan_members_url = f"https://data.aoe2companion.com/api/profiles?language=es&clan=DYNB&extend=profiles.avatar_medium_url&page={clan_members_page}"
        response = requests.get(clan_members_url, headers=api_headers)
        if response.status_code != 200:
            return []
        data = response.json()
        for player in data['profiles']:
            member = Member(
                id=player['profileId'],
                name=player['name'],
                avatar_url=player['avatarMediumUrl'],
                total_games=player['games'],
                flag=player['country'],
                leaderboard={}
            )
            members.append(member)
        clan_members_page += 1
        if not data['hasMore']:
            break

    response_1v1 = requests.get(clan_1v1_url, headers=api_headers)
    if response_1v1.status_code == 200:
        data_1v1 = response_1v1.json()
        members = get_leaderboard_data(members, data_1v1)

    response_tg = requests.get(clan_tg_url, headers=api_headers)
    if response_tg.status_code == 200:
        data_tg = response_tg.json()
        members = get_leaderboard_data(members, data_tg)

    return members


def write_members_to_sheet(member_list: list[Member], sheet_document):
    # Clear existing content
    sheet_document.clear()

    # Prepare headers
    headers = ["Nombre", "Total Partidas", "País",
               "ELO 1v1", "Max ELO 1v1", "Partidas 1v1", "Victorias 1v1", "Winrate 1v1", "Última Partida 1v1",
               "ELO TG", " Max ELO TG", "Partidas TG", "Victorias TG", "Winrate TG", "Última Partida TG"
               ]

    # Prepare data rows
    data_rows = [headers]

    for member in member_list:
        # Get 1v1 leaderboard data if available
        lb_1v1 = member.leaderboard.get('rm_1v1')
        # Get team leaderboard data if available
        lb_tg = member.leaderboard.get('rm_team')

        row = [
            member.name,
            member.total_games,
            country_code_to_flag(member.flag),
            # 1v1 data
            lb_1v1.elo if lb_1v1 else "",
            lb_1v1.max_elo if lb_1v1 else "",
            lb_1v1.total_games if lb_1v1 else "",
            lb_1v1.wins if lb_1v1 else "",
            f"{lb_1v1.winrate:.2%}" if lb_1v1 else "",
            date_transform(lb_1v1.last_match) if lb_1v1 else "",
            # Team data
            lb_tg.elo if lb_tg else "",
            lb_tg.max_elo if lb_tg else "",
            lb_tg.total_games if lb_tg else "",
            lb_tg.wins if lb_tg else "",
            f"{lb_tg.winrate:.2%}" if lb_tg else "",
            date_transform(lb_tg.last_match) if lb_tg else ""
        ]
        data_rows.append(row)

    # Write to sheet
    sheet_document.update(range_name="A1", values=data_rows)


if __name__ == "__main__":
    all_members = get_members()
    gc = gspread.authorize(creds)
    sheet = gc.open("AoE 2 Clan Dynamic").sheet1
    write_members_to_sheet(all_members, sheet)
    print("Dynamic Clan Members updated successfully ✅")
