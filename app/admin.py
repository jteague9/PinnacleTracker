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
    list_display = ("matchup_id", "get_tournament_name", "home_player", "away_player", "start_time", "winner")
    readonly_fields = ("created_at", "modified_at")
    search_fields = ("matchup_id", "tournament__tournament_id", "tournament__name", "home_player", "away_player")
    ordering = ("-created_at",)

    def get_tournament_name(self, obj):
        return obj.tournament.name

    get_tournament_name.short_description = 'tournament name'
    get_tournament_name.admin_order_field = 'tournament__name'


@admin.register(Period)
class PeriodAdmin(admin.ModelAdmin):
    list_display = ("matchup", "period")
    readonly_fields = ("created_at", "modified_at")
    search_fields = ("matchup__matchup_id",)
    ordering = ("-created_at",)


admin.register(MoneylineRecord)
