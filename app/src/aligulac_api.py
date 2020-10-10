import uplink
import requests
from os import environ as env

BASE_URL = "http://aligulac.com/api/v1/"
API_KEY = env.get('ALIGULAC_KEY')


class AligulacAPI(uplink.Consumer):

    def __init__(self, base_url):
        super(AligulacAPI, self).__init__(base_url=base_url)

    @uplink.get("match/?pla__in={player_a},{player_b}&plb__in={player_a},{player_b}&apikey={api_key}&order_by=-date")
    def get_match_history(self, player_a: int, player_b: int, api_key: str = API_KEY):
        """Gets match history between 2 players"""

    @staticmethod
    def get_player(query: str):
        return requests.get(f'http://aligulac.com/search/json/?q={query}')

