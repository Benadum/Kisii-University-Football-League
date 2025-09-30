# backend/api/urls.py
from django.urls import path
from .views import (
    TeamStandingsViewSet, 
    FixturesListView, 
    ResultsListView, 
    TopScorersListView,
    TeamFormView
)

urlpatterns = [
    path('standings/', TeamStandingsViewSet.as_view({'get': 'list'}), name='team-standings'),
    path('fixtures/', FixturesListView.as_view(), name='fixtures-list'),
    path('results/', ResultsListView.as_view(), name='results-list'),
    path('top-scorers/', TopScorersListView.as_view(), name='top-scorers-list'),
    path('teams/<int:pk>/form/', TeamFormView.as_view(), name='team-form'),
]