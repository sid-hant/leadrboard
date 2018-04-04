from django import forms
from django.contrib.auth import get_user_model
from .models import Player, Match


class addPlayerForm(forms.ModelForm):
    class Meta():
        model = Player
        fields = ('name',)
        labels = {
            'name': 'Name'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class addMatchForm(forms.ModelForm):
    class Meta():
        model = Match
        fields = ('p1_name','p2_name','p1_score', 'p2_score',)
        labels = {
            'p1_name': 'Home Player Name','p2_name': 'Away Player Name','p1_score': 'Home Score', 'p2_score':'Away Score'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class delPlayerForm(forms.ModelForm):
    class Meta():
        model = Player
        fields = ('name',)
        labels = {
            'name': 'Name'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
