# api/forms.py
from django import forms
from .models import Player

class PlayerAdminForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = '__all__' # Use all fields from the Player model

    def clean(self):
        # This 'clean' method is run during form validation
        cleaned_data = super().clean()
        goals = cleaned_data.get("goals")
        team = cleaned_data.get("team")

        if goals is not None and team is not None:
            if goals > team.goals_for:
                # This is the key part. We raise a ValidationError on a specific field.
                # This will show the error message right under the 'goals' field.
                raise forms.ValidationError({
                    'goals': f"Player goals ({goals}) cannot exceed the team's total goals for ({team.goals_for})."
                })
        
        return cleaned_data