from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic import ListView, UpdateView, DeleteView, CreateView

from braces.views import LoginRequiredMixin

from user.models import UserStatus
from .models import Lobby
from .forms import LobbyCreationForm


class LobbyCreateView(LoginRequiredMixin, CreateView):

    template_name = 'lobby_creation.html'
    form_class = LobbyCreationForm
    succes_url = '/hole/'

    def form_valid(self, form):
        lobby = form.save(commit=False)
        lobby.creator = self.request.user
        lobby.save()
        lobby.players.add(self.request.user)

        return super(LobbyCreateView, self).form_valid(form)


class LobbyListView(LoginRequiredMixin, ListView):

    template_name = 'lobby_list.html'
    ordering = '-created'
    queryset = Lobby.objects.all()
    context_object_name = 'lobby_list'

    def get_context_data(self, **kwargs):
        user_status = UserStatus.objects.filter(
            player=self.request.user.id, timeout__isnull=False)

        context = super(LobbyListView, self).get_context_data(**kwargs)

        if user_status:
            print(type(datetime.now()), type(user_status[0].timeout))
            td = datetime.now() - (user_status[0].timeout).replace(tzinfo=None)

            if td.total_seconds() < 60:
                context['timeout'] = True

        context['player_lobby'] = self.queryset.filter(
            players=self.request.user.id)
        if self.queryset.filter(
                creator=self.request.user.id, status=1).exists():
            context['in_lobby'] = True

        return context


class OnlinePlayerListView(LoginRequiredMixin, ListView):

    context_object_name = 'online'
    queryset = UserStatus.objects.all().order_by('player__username')
    template_name = 'userstatus_list.html'


class LobbyDeleteView(DeleteView):

    model = Lobby
    success_url = '/hole/'


class LobbyAddPlayer(LoginRequiredMixin, UpdateView):

    model = Lobby

    def dispatch(self, request, *args, **kwargs):
        lobby = Lobby.objects.get(pk=kwargs['pk'])
        lobby.players.add(request.user.id)

        return redirect('lobby:hole')


def index(request):
    if request.user is not None:

        return redirect('lobby:hole')

    return redirect('user:login')


@login_required(login_url='user:login')
def lobby_hole(request):
    context = RequestContext(request)

    return render_to_response('lobby_hole.html', context)


@login_required(login_url='user:login')
def in_lobby(request):
    context = RequestContext(request)
    lobby = Lobby.objects.filter(players=request.user.id)

    return render_to_response('in_lobby.html',
                              {'lobby': lobby},
                              context)


@login_required(login_url='user:login')
def leave_lobby(request, pk):

    if request.method == 'POST':

        lobby = Lobby.objects.get(pk=pk)
        lobby.players.remove(request.user.id)

    return redirect('lobby:hole')
