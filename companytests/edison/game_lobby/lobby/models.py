from datetime import datetime

from django.db import models
from django.core.exceptions import ValidationError
from django.dispatch import receiver
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.db.models.signals import m2m_changed
from django.utils.translation import ugettext_lazy as _

import user


NUMBER_OF_PLAYERS_CHOICES = (('2', 'один на один'),
                             ('4', 'четыре игрока'))

STATUS = (('0', 'набор участников'),
          ('1', 'набор окончен'),
          ('2', 'идёт игра'))


class Lobby(models.Model):

    creator = models.OneToOneField(
        User, unique=True, blank=True, null=True, verbose_name='создатель арены', related_name='creator')
    players = models.ManyToManyField(
        User, verbose_name='присоединившиеся игроки', related_name='players_in_the_lobby')
    name = models.CharField(
        max_length=100, unique=True, null=False, verbose_name='название лобби')
    number = models.CharField(
        max_length=1, choices=NUMBER_OF_PLAYERS_CHOICES, verbose_name=_('тип лобби'))
    status = models.CharField(
        max_length=1, choices=STATUS, default='0', verbose_name='готовность лобби')
    created = models.DateTimeField(
        editable=False, auto_now_add=True, null=True)
    modified = models.DateTimeField(null=True, blank=True, auto_now=True)

    def get_absolute_url(self):
        return reverse('lobby:hole')


@receiver(m2m_changed, sender=Lobby.players.through)
def players_changed(sender, action, **kwargs):

    lobby = kwargs.pop('instance', None)

    if action == 'post_add':

        if lobby.players.count() > int(lobby.number):
            raise ValidationError(
                _('В лобби уже максимальное количество игроков'))

        if int(lobby.number) == lobby.players.count():
            lobby.status = '1'
            lobby.save()

    if action == 'post_remove':

        if not lobby.players.count() or lobby.creator is None:
            lobby.delete()

        else:
            lobby.status = '0'
            id = list(kwargs['pk_set'])[0]
            user_out = user.models.UserStatus.objects.get(player=id)
            user_out.timeout = datetime.now()
            user_out.save()
            lobby.save()

