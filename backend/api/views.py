# backend/api/views.py
from rest_framework import viewsets, generics, permissions # <-- IMPORTED
from .models import Team, Player, Match
from .serializers import TeamStandingsSerializer, PlayerSerializer, MatchSerializer
from django.db.models import F
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response

class TeamStandingsViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TeamStandingsSerializer
    permission_classes = [permissions.AllowAny] # <-- ADDED
    def get_queryset(self):
        return Team.objects.annotate(
            calculated_points=F('wins') * 3 + F('draws'),
            calculated_gd=F('goals_for') - F('goals_against')
        ).order_by('-calculated_points', '-calculated_gd', 'name')

class FixturesListView(generics.ListAPIView):
    serializer_class = MatchSerializer
    permission_classes = [permissions.AllowAny] # <-- ADDED
    def get_queryset(self):
        return Match.objects.filter(status='SCHEDULED', match_date__gte=timezone.now()).order_by('match_date')

class ResultsListView(generics.ListAPIView):
    serializer_class = MatchSerializer
    permission_classes = [permissions.AllowAny] # <-- ADDED
    def get_queryset(self):
        return Match.objects.filter(status='PLAYED', match_date__lte=timezone.now()).order_by('-match_date')[:5]

class TopScorersListView(generics.ListAPIView):
    serializer_class = PlayerSerializer
    permission_classes = [permissions.AllowAny] # <-- ADDED
    def get_queryset(self):
        return Player.objects.filter(goals__gt=0).order_by('-goals')[:10]

class TeamFormView(APIView):
    permission_classes = [permissions.AllowAny] # <-- ADDED
    def get(self, request, pk, format=None):
        try:
            team = Team.objects.get(pk=pk)
        except Team.DoesNotExist:
            return Response({"error": "Team not found"}, status=404)
        
        form = []
        last_5_matches = (team.home_matches.filter(status='PLAYED') | team.away_matches.filter(status='PLAYED')).distinct().order_by('-match_date')[:5]
        for match in last_5_matches:
            if match.home_team == team:
                if match.home_score > match.away_score: form.append('W')
                elif match.home_score < match.away_score: form.append('L')
                else: form.append('D')
            else:
                if match.away_score > match.home_score: form.append('W')
                elif match.away_score < match.home_score: form.append('L')
                else: form.append('D')
        return Response(form)