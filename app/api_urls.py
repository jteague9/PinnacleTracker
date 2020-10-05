from django.urls import path
from app import views
from rest_framework.schemas import get_schema_view

schema_view = get_schema_view(title="SC2 Lines API", version="1.0.0")

urlpatterns = [
    path('schema/', schema_view),
    path('tournaments/', views.TournamentList.as_view()),
    path('tournaments/<int:tournament_id>/', views.TournamentDetail.as_view()),
    path('matchups/', views.MatchupList.as_view()),
    path('matchups/<int:matchup_id>/', views.MatchupDetail.as_view()),
    path('matchups/<int:matchup_id>/period/<int:period_id>/', views.PeriodDetail.as_view()),
    path('latest/', views.LatestPeriodsList.as_view()),
]
