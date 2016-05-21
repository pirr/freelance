from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in
from django.contrib.auth.signals import user_logged_out

from lobby.models import Lobby


class UserStatus(models.Model):
    player = models.OneToOneField(
        User, unique=True, verbose_name='игрок в сети')
    timeout = models.DateTimeField(null=True, blank=True)


def player_logged(sender, user, **kwargs):

    if user != User.objects.get(username='admin'):
        UserStatus.objects.create(player=user)

user_logged_in.connect(player_logged)


def player_logout(sender, user, **kwargs):
    UserStatus.objects.filter(player=user).delete()
    try:
        Lobby.objects.filter(creator=user.id).delete()
    except:
        print('player had not lobby')

user_logged_out.connect(player_logout)
