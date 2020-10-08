from app.src.pinnacleapi import PinnacleAPI, BASE_URL
from app.models import *
from os import environ as env

API_KEY = env['API_KEY']
ESPORTS_ID = '12'


def fetch_moneylines():
    client = PinnacleAPI(BASE_URL, API_KEY)
    esports = client.get_leagues(ESPORTS_ID).json()

    for league in esports:
        if league['name'].startswith('StarCraft 2'):
            league_id = league['id']
            matchups = client.get_matchups(league_id).json()
            straights = client.get_straights(league_id).json()
            for matchup in matchups:
                if matchup['type'] != 'matchup':
                    continue
                for straight in straights:
                    if straight['type'] != 'moneyline':
                        continue
                    if matchup.get('id') == straight.get('matchupId'):
                        moneyline_record = _add_moneyline_record(matchup, straight)
                        _delete_middle_record(moneyline_record.period)


def purge_duplicate_ml_records():
    periods = Period.objects.all()
    for p in periods:
        while _delete_middle_record(p):
            print(f'deleted pricepoint for {p}')


def _add_moneyline_record(matchup: dict, straight: dict) -> MoneylineRecord:
    tournament = matchup['league']
    tournament_name = tournament['name'].split('StarCraft 2 - ')[-1]
    tournament_id = tournament['id']

    t, _ = Tournament.objects.update_or_create(tournament_id=tournament_id, defaults={'name': tournament_name})

    matchup_id = matchup['id']
    home_player = [p['name'] for p in matchup['participants'] if p['alignment'] == 'home'][0]
    away_player = [p['name'] for p in matchup['participants'] if p['alignment'] == 'away'][0]
    start_time = matchup['startTime']
    m, _ = Matchup.objects.update_or_create(tournament=t, matchup_id=matchup_id, defaults={
        'home_player': home_player, 'away_player': away_player, 'start_time': start_time
    })

    period = straight['period']
    p, _ = Period.objects.get_or_create(matchup=m, period=period)

    home_price = [p['price'] for p in straight['prices'] if p['designation'] == 'home'][0]
    away_price = [p['price'] for p in straight['prices'] if p['designation'] == 'away'][0]

    print("adding moneyline record", p)
    return MoneylineRecord.objects.create(home_price=home_price, away_price=away_price, period=p)


def _delete_middle_record(period: Period) -> bool:
    recent_records = MoneylineRecord.objects.filter(period=period).order_by('-created_at')
    if len(recent_records) > 2:
        last, second, third = recent_records[0:3]
        if second.is_duplicate(last) and second.is_duplicate(third):
            second.delete()
            return True
    return False


def count_db_entries():
    count = 0
    count += MoneylineRecord.objects.all().count()
    count += Period.objects.all().count()
    count += Matchup.objects.all().count()
    count += Tournament.objects.all().count()
    return count


def purge_records_until_limit(limit: int):
    print("reduce until", limit)
    while count_db_entries() >= limit:
        last_matchup = Matchup.objects.all().order_by('start_time').first()
        print("deleting matchup...", last_matchup)
        last_matchup.delete()

    # delete tournaments which no longer relate to any matchups
    for tournament in Tournament.objects.all():
        if Matchup.objects.filter(tournament=tournament).count() == 0:
            print("deleting tournament... ", tournament.name)
            tournament.delete()


if __name__ == "__main__":
    fetch_moneylines()
