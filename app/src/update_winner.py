from app.src.aligulac_api import AligulacAPI, BASE_URL
from app.models import Matchup, Period
from django.utils import timezone


def _get_player_id(name: str) -> int:
    response = AligulacAPI.get_player(name.lower()).json()
    for p in response['players']:
        if p['tag'].lower() == name.lower():
            return p['id']


def _get_correct_matchup(matchup: Matchup, matchup_list: list) -> dict:
    periods = Period.objects.filter(matchup=matchup)
    period_count = max([p.period for p in periods])
    d = matchup.start_time
    for mu in matchup_list:
        winner_game_count = max(mu['sca'], mu['scb'])
        if mu['date'] == f"{d.year}-{d.month:02}-{d.day:02}"\
           and period_count == (winner_game_count * 2) - 1:
            return mu


def get_matchup_winner(matchup: Matchup) -> str:
    home_player = matchup.home_player
    away_player = matchup.away_player
    home_id = _get_player_id(home_player)
    away_id = _get_player_id(away_player)
    client = AligulacAPI(BASE_URL)
    r = client.get_match_history(home_id, away_id)
    response = r.json()
    correct_match = _get_correct_matchup(matchup, response['objects'])

    try:
        winner = _get_winner(correct_match)
        # use the same capitalization as in our db
        if winner.lower() == home_player.lower():
            return home_player
        if winner.lower() == away_player.lower():
            return away_player
    except:
        pass


def _get_winner(match: dict) -> str:
    if match['sca'] > match['scb']:
        return match['pla']['tag']
    if match['scb'] > match['sca']:
        return match['plb']['tag']


def update_all_winners():
    # filter to closed matchups with no assigned winner
    for matchup in Matchup.objects.filter(start_time__lt=timezone.now(), winner=None):
        print(matchup)
        winner = get_matchup_winner(matchup)
        print(winner)
        matchup.winner = winner
        matchup.save()

