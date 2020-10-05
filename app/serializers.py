from app.models import Tournament, Matchup, Period, MoneylineRecord
from rest_framework import serializers


class TournamentSerializer(serializers.ModelSerializer):
    created = serializers.DateTimeField(source='created_at')

    class Meta:
        model = Tournament
        fields = ['tournament_id', 'name', 'matchups', 'created']


class MatchupSerializer(serializers.ModelSerializer):
    tournament_id = serializers.IntegerField(source='tournament.tournament_id')
    periods = serializers.SlugRelatedField(many=True, read_only=True, slug_field='period')
    created = serializers.DateTimeField(source='created_at')

    class Meta:
        model = Matchup
        fields = ['tournament_id', 'matchup_id', 'home_player', 'away_player',
                  'periods', 'start_time', 'open', 'created']


class BettingOddsField(serializers.Field):

    def to_representation(self, obj):
        odds_format = self.context['request'].query_params.get('odds')
        if odds_format and odds_format.lower() == 'decimal':
            return round(obj / 100 + 1 if obj > 0 else -100 / obj + 1, 3)
        if odds_format and odds_format.lower() == 'percent':
            return round(100 / (obj + 100) if obj > 0 else -obj / (-obj + 100), 3)
        return obj


class MoneylineRecordSerializer(serializers.ModelSerializer):
    recorded_at = serializers.DateTimeField(source='created_at')
    home_price = BettingOddsField()
    away_price = BettingOddsField()

    class Meta:
        model = MoneylineRecord
        fields = ['home_price', 'away_price', 'recorded_at']


class PeriodSerializer(serializers.ModelSerializer):
    home_player = serializers.CharField(source='matchup.home_player')
    away_player = serializers.CharField(source='matchup.away_player')
    moneylines = MoneylineRecordSerializer(many=True, read_only=True)

    class Meta:
        model = Period
        fields = ['period', 'home_player', 'away_player', 'moneylines']


class BriefMatchupSerializer(serializers.ModelSerializer):
    home_price = BettingOddsField(source='get_latest_mlr.home_price')
    away_price = BettingOddsField(source='get_latest_mlr.away_price')
    tournament = serializers.CharField(source='matchup.tournament.name')
    home_player = serializers.CharField(source='matchup.home_player')
    away_player = serializers.CharField(source='matchup.away_player')
    start_time = serializers.DateTimeField(source='matchup.start_time')

    class Meta:
        model = Period
        fields = ['tournament', 'home_player', 'away_player', 'home_price', 'away_price', 'start_time']
