from django.contrib import admin
from app.models import Tournament, Matchup, Period, MoneylineRecord


@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    list_display = ("tournament_id", "name")
    readonly_fields = ("created_at", "modified_at")
    search_fields = ("tournament_id", "name")
    ordering = ("-created_at",)


@admin.register(Matchup)
class MatchupAdmin(admin.ModelAdmin):
    list_display = ("matchup_id", "tournament", "home_player", "away_player", "start_time", "winner")
    readonly_fields = ("created_at", "modified_at")
    search_fields = ("matchup_id", "tournament__tournament_id", "home_player", "away_player")
    ordering = ("-created_at",)


@admin.register(Period)
class PeriodAdmin(admin.ModelAdmin):
    list_display = ("matchup", "period")
    readonly_fields = ("created_at", "modified_at")
    search_fields = ("matchup__matchup_id",)
    ordering = ("-created_at",)


admin.register(MoneylineRecord)
