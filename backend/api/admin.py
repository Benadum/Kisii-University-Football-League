# api/admin.py
from django.contrib import admin
from .models import Team, Player, Match
from .forms import PlayerAdminForm

# This decorator registers the Team model with the TeamAdmin class
@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'captain', 'matches_played', 'wins', 'draws', 'losses')
    readonly_fields = ('matches_played', 'wins', 'draws', 'losses', 'goals_for', 'goals_against')
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "captain":
            team_id = request.resolver_match.kwargs.get('object_id')
            if team_id:
                kwargs["queryset"] = Player.objects.filter(team_id=team_id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

# This decorator registers the Player model with our new PlayerAdmin class
@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    form = PlayerAdminForm # Use our custom form for validation
    list_display = ('first_name', 'last_name', 'team', 'goals')
    list_filter = ('team',)

# This registers the Match model normally
admin.site.register(Match)

