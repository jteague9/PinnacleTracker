from django.db import models
from datetime import datetime


class Tournament(models.Model):
    tournament_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30)
    created_at: datetime = models.DateTimeField(auto_now_add=True)
    modified_at: datetime = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']


class Matchup(models.Model):
    matchup_id = models.IntegerField(primary_key=True)
    tournament = models.ForeignKey(Tournament, related_name='matchups', on_delete=models.CASCADE)
    home_player = models.CharField(max_length=30)
    away_player = models.CharField(max_length=30)
    start_time: datetime = models.DateTimeField(null=True, blank=True)
    created_at: datetime = models.DateTimeField(auto_now_add=True)
    modified_at: datetime = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Matchup(home:{self.home_player}, away:{self.away_player}, tournament:{self.tournament.name})"


class Period(models.Model):
    matchup = models.ForeignKey(Matchup, related_name='periods', on_delete=models.CASCADE)
    period = models.IntegerField()
    created_at: datetime = models.DateTimeField(auto_now_add=True)
    modified_at: datetime = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['period']

    def __str__(self):
        return f"Period(matchup:{self.matchup}, period:{self.period})"


class MoneylineRecord(models.Model):
    home_price = models.IntegerField()
    away_price = models.IntegerField()
    period = models.ForeignKey(Period, related_name='moneylines', on_delete=models.CASCADE)
    created_at: datetime = models.DateTimeField(auto_now_add=True)
    modified_at: datetime = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def is_duplicate(self, obj):
        return self.period == obj.period and self.home_price == obj.home_price and self.away_price == obj.away_price
