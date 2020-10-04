from app.models import *
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
        fields = ['tournament_id', 'matchup_id', 'home_player', 'away_player', 'periods', 'start_time', 'created']


class MoneylineRecordSerializer(serializers.ModelSerializer):
    recorded_at = serializers.DateTimeField(source='created_at')

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

