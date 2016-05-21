from .models import Lobby, NUMBER_OF_PLAYERS_CHOICES
from django import forms
from django.forms.widgets import TextInput, Select
from django.utils.translation import ugettext_lazy as _


class LobbyCreationForm(forms.ModelForm):

    name = forms.CharField(label='', widget=TextInput(
        attrs={'class': 'form-control', 'placeholder': _('Название лобби')}))
    number = forms.ChoiceField(label='', choices=NUMBER_OF_PLAYERS_CHOICES,
                               widget=Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Lobby
        fields = ('name', 'number')