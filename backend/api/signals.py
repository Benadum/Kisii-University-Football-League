# api/signals.py
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Match, Team

def recalculate_all_team_stats(team):
    """
    A helper function to completely recalculate a single team's stats
    by looking at all of its played matches.
    """
    if team is None:
        return

    # Reset all stats to zero before recounting
    team.matches_played = 0
    team.wins = 0
    team.draws = 0
    team.losses = 0
    team.goals_for = 0
    team.goals_against = 0
    
    # Recalculate based on home matches
    for match in team.home_matches.filter(status='PLAYED'):
        if match.home_score is not None and match.away_score is not None:
            team.matches_played += 1
            team.goals_for += match.home_score
            team.goals_against += match.away_score
            if match.home_score > match.away_score:
                team.wins += 1
            elif match.home_score < match.away_score:
                team.losses += 1
            else:
                team.draws += 1

    # Recalculate based on away matches
    for match in team.away_matches.filter(status='PLAYED'):
        if match.home_score is not None and match.away_score is not None:
            team.matches_played += 1
            team.goals_for += match.away_score
            team.goals_against += match.home_score
            if match.away_score > match.home_score:
                team.wins += 1
            elif match.away_score < match.home_score:
                team.losses += 1
            else:
                team.draws += 1
    
    # Save the updated team object to the database
    team.save()

# This function will run every time a Match object is saved.
@receiver(post_save, sender=Match)
def update_team_stats_on_save(sender, instance, **kwargs):
    """
    After a Match is saved, recalculate the standings for both teams.
    """
    # We only care about matches that have been played
    if instance.status == 'PLAYED':
        recalculate_all_team_stats(instance.home_team)
        recalculate_all_team_stats(instance.away_team)

# This function will run if a Match object is ever deleted.
@receiver(post_delete, sender=Match)
def update_team_stats_on_delete(sender, instance, **kwargs):
    """
    After a Match is deleted, recalculate the standings for both teams.
    """
    recalculate_all_team_stats(instance.home_team)
    recalculate_all_team_stats(instance.away_team)