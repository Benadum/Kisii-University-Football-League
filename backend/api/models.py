# api/models.py
from django.db import models
from django.core.exceptions import ValidationError # <-- Import this


class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    logo = models.ImageField(upload_to='team_logos/', null=True, blank=True)
    
    captain = models.OneToOneField(
        'Player', # The model to link to is Player
        on_delete=models.SET_NULL, # If the player is deleted, the captain field becomes empty (null)
        null=True, # The field is allowed to be empty in the database
        blank=True, # The field is optional in the Django admin
        related_name='captain_of' # Helps access the team from the player instance
    )
    # Add these new fields
    matches_played = models.IntegerField(default=0)
    wins = models.IntegerField(default=0)
    draws = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    goals_for = models.IntegerField(default=0)
    goals_against = models.IntegerField(default=0)

    # Property to calculate Goal Difference
    @property
    def goal_difference(self):
        return self.goals_for - self.goals_against

    # Property to calculate Points
    @property
    def points(self):
        return (self.wins * 3) + self.draws

    def __str__(self):
        return self.name

# ... Player model remains the same ...
class Player(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    
    # ID Number is now REQUIRED
    # unique=True ensures no two players can have the same ID number.
    id_number = models.CharField(max_length=50, unique=True)
    
    position = models.CharField(max_length=50)
    
    # Player photo can remain optional
    photo = models.ImageField(upload_to='player_photos/', null=True, blank=True)
    
    # ID Photo is now REQUIRED
    id_photo = models.ImageField(upload_to='player_id_photos/', null=True)

    team = models.ForeignKey(Team, related_name='players', on_delete=models.CASCADE)
    goals = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    team = models.ForeignKey(Team, related_name='players', on_delete=models.CASCADE)
    goals = models.IntegerField(default=0)

    # 2. ADD THIS ENTIRE METHOD
    def save(self, *args, **kwargs):
        # Check if the player's team exists and if goals exceed the team's total
        if self.team and self.goals > self.team.goals_for:
            raise ValidationError(f"Validation Error: Player goals ({self.goals}) cannot exceed their team's total goals for ({self.team.goals_for}).")
        super().save(*args, **kwargs) # This calls the original save method

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Match(models.Model):
    STATUS_CHOICES = [
        ('SCHEDULED', 'Scheduled'),
        ('PLAYED', 'Played'),
    ]

    home_team = models.ForeignKey(Team, related_name='home_matches', on_delete=models.CASCADE)
    away_team = models.ForeignKey(Team, related_name='away_matches', on_delete=models.CASCADE)
    home_score = models.IntegerField(null=True, blank=True)
    away_score = models.IntegerField(null=True, blank=True)
    match_date = models.DateTimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='SCHEDULED')

    def __str__(self):
        return f"{self.home_team} vs {self.away_team} on {self.match_date.strftime('%Y-%m-%d')}"