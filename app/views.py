from app.models import Tournament, Matchup, Period
from app.serializers import TournamentSerializer, MatchupSerializer, PeriodSerializer, BriefMatchupSerializer
from rest_framework import generics
from django.http import Http404
from django.db.models import Q
from django.utils import timezone


class TournamentList(generics.ListAPIView):
    serializer_class = TournamentSerializer
    lookup_field = 'tournament_id'

    def get_queryset(self):
        name = self.request.query_params.get('name')
        tournament_filter = Q()
        if name:
            tournament_filter &= Q(name__icontains=name)
        return Tournament.objects.filter(tournament_filter)


class TournamentDetail(generics.RetrieveAPIView):
    queryset = Tournament.objects.all()
    serializer_class = TournamentSerializer
    lookup_field = 'tournament_id'


class MatchupList(generics.ListAPIView):
    serializer_class = MatchupSerializer
    lookup_field = 'matchup_id'

    def get_queryset(self):
        player = self.request.query_params.get('player')
        is_open = self.request.query_params.get('open')
        matchup_filter = Q()
        if player:
            matchup_filter &= Q(home_player__iexact=player) | Q(away_player__iexact=player)
        if is_open is not None:
            if is_open.lower() == 'false':
                matchup_filter &= Q(start_time__lt=timezone.now())
            if is_open.lower() == 'true':
                matchup_filter &= Q(start_time__gt=timezone.now())
        return Matchup.objects.filter(matchup_filter)


class MatchupDetail(generics.RetrieveAPIView):
    queryset = Matchup.objects.all()
    serializer_class = MatchupSerializer
    lookup_field = 'matchup_id'


class PeriodDetail(generics.RetrieveAPIView):
    queryset = Period.objects.all()
    serializer_class = PeriodSerializer

    def get_object(self):
        matchup_id = self.kwargs.get('matchup_id')
        period_id = self.kwargs.get('period_id')
        try:
            return Period.objects.get(matchup__matchup_id=matchup_id, period=period_id)
        except Period.DoesNotExist:
            raise Http404


class LatestPeriodsList(generics.ListAPIView):
    serializer_class = BriefMatchupSerializer
    queryset = Period.objects.filter(matchup__start_time__gt=timezone.now(), period=0)
