from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput
from django.utils.translation import ugettext_lazy as _


class RFPAuthForm(AuthenticationForm):

    username = forms.CharField(label='', widget=TextInput(
        attrs={'class': 'form-control', 'placeholder': _('Имя')}))
    password = forms.CharField(label='', widget=PasswordInput(
        attrs={'class': 'form-control', 'placeholder': _('Пароль')}))
