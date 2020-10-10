import uplink

BASE_URL = "https://guest.api.arcadia.pinnacle.com/0.1/"


class PinnacleAPI(uplink.Consumer):

    def __init__(self, base_url, api_key):
        super(PinnacleAPI, self).__init__(base_url=base_url)
        self.session.headers['x-api-key'] = api_key

    @uplink.get("sports/{sport_id}/leagues")
    def get_leagues(self, sport_id: str):
        """Get leagues by sport id"""

    @uplink.get("leagues/{league_id}/matchups")
    def get_matchups(self, league_id: str):
        """Get matchups by league id"""

    @uplink.get("leagues/{league_id}/markets/straight")
    def get_straights(self, league_id: str):
        """Get straights by league id"""
