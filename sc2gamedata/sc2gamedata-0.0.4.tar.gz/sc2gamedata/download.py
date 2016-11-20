import json
import typing
import urllib.request
import multiprocessing
import functools
import itertools

from . import GameData

_game_data_resource = "https://us.api.battle.net/data/sc2"
_queue_id_1v1 = "201"
_team_type_arranged = "0"

_league_ids = range(6)


def _get_game_data(access_token: str, path: str) -> dict:
    with urllib.request.urlopen(_game_data_resource + path + "?access_token=" + access_token) as response:
        response_str = response.read().decode('utf8')
    return json.loads(response_str)


def get_current_season_data(access_token: str) -> dict:
    return _get_game_data(access_token, "/season/current")


def get_league_data(access_token: str, season: int, league_id: int) -> dict:
    path = "/league/{}/{}/{}/{}".format(season, _queue_id_1v1, _team_type_arranged, league_id)
    return _get_game_data(access_token, path)


def get_ladder_data(access_token: str, ladder_id: int) -> dict:
    path = "/ladder/{}".format(ladder_id)
    return _get_game_data(access_token, path)


def _extract_tiers(league_data) -> list:
    return list(reversed(league_data["tier"]))


def _extract_divisions(tier_id, tier_data) -> list:
    result = tier_data["division"]
    for division in result:
        division["tier_id"] = tier_id
    return result


def _extract_ladders(access_token: str, division_index: int, division_data: dict) -> dict:
    result = get_ladder_data(access_token, division_data["ladder_id"])
    result["division_index"] = division_index
    return result


def _extract_teams(ladder_index, ladder_data):
    result = ladder_data["team"]
    for result_entry in result:
        result_entry["ladder_index"] = ladder_index

    return result


def get_game_data(access_token: str, workers: int = 10) -> GameData:
    current_season_id = get_current_season_data(access_token)["id"]

    with multiprocessing.Pool(workers) as p:
        leagues = p.map(functools.partial(get_league_data, access_token, current_season_id), range(len(_league_ids)))
        tiers = list(itertools.chain.from_iterable(p.map(_extract_tiers, leagues)))
        divisions = list(itertools.chain.from_iterable(p.starmap(_extract_divisions, enumerate(tiers))))
        ladders = p.starmap(functools.partial(_extract_ladders, access_token), enumerate(divisions))
        teams = list(itertools.chain.from_iterable(p.starmap(_extract_teams, enumerate(ladders))))

    return GameData(leagues, tiers, divisions, ladders, teams)

