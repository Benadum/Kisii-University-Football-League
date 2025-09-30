# api/serializers.py
from rest_framework import serializers
from .models import Team, Player, Match

# A simple serializer for nesting within other serializers
class TeamNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['name']

# -----------------
# THE CORRECTION IS HERE
# -----------------
# We must define CaptainSerializer BEFORE it is used in TeamStandingsSerializer.
class CaptainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ['first_name', 'last_name']

class PlayerSerializer(serializers.ModelSerializer):
    team = TeamNameSerializer(read_only=True)
    class Meta:
        model = Player
        fields = ['id', 'first_name', 'last_name', 'id_number','id_photo','team', 'goals']

class MatchSerializer(serializers.ModelSerializer):
    home_team = TeamNameSerializer(read_only=True)
    away_team = TeamNameSerializer(read_only=True)
    class Meta:
        model = Match
        fields = ['id', 'home_team', 'away_team', 'home_score', 'away_score', 'match_date', 'status']

# This is the full serializer for the main standings table
class TeamStandingsSerializer(serializers.ModelSerializer):
    # This line will now work because CaptainSerializer is defined above
    captain = CaptainSerializer(read_only=True)

    class Meta:
        model = Team
        fields = [
            'id', 'name', 'logo', 'captain', # Added captain here
            'matches_played', 'wins', 'draws', 
            'losses', 'goals_for', 'goals_against', 'goal_difference', 'points'
        ]