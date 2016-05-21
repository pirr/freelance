from django.test import TestCase
from .forms import LobbyCreationForm
from django.contrib.auth.models import User
from unittest.mock import patch
from . import GeolDoc


class LobbyTest(TestCase):

    def test_register_form(self, username='player_1', password='1'):
        resp = self.client.post('/user/register/', {'username': username,
                                                    'password': password})
        self.assertEqual(resp.status_code, 200)

    @patch('lobby.models.players_changed')
    def test_players_changed_posted_signal_triggered():

        creator = User.objects.create(username='creator', password='1')
        player = User.objects.create(username='player', password='1')
        lobby_params = {'name': 'lobby_1', 'number': '2'}

        form = LobbyCreationForm(lobby_params)

        lobby = form.save(commit=False)
        lobby.creator = creator
        lobby.save()
        lobby.players.add(creator)
        lobby.players.add(player)
        print(lobby.players.count())

        self.assertTrue(mock.called)
        self.assertEqual(mock.call_count, 1)

        print('ok')
