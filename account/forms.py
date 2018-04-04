from django import forms
from django.contrib.auth import get_user_model

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = get_user_model()
        fields = ('username', 'password')
        labels = {
            'username': 'Room Name',
            'password': 'PASSWORD'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
