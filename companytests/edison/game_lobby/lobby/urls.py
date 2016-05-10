from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^hole/', views.lobby_hole, name='hole'),
    url(r'^creation/$', views.LobbyCreateView.as_view(), name='lobby_creation'),
    url(r'^enjoy/(?P<pk>\d+)/$', views.LobbyAddPlayer.as_view(), name='take_lobby'),
    url(r'^get_lobbys/', views.LobbyListView.as_view(), name='get_lobbys'),
    url(r'^leave_lobby/(?P<pk>\d+)/$', views.leave_lobby, name='leave_lobby'),
    url(r'^inside/', views.in_lobby, name='in_lobby'),
    url(r'^online/', views.OnlinePlayerListView.as_view(), name='online'),
    # url(r'^inside/', views.InLobby.as_view(), name='in_lobby')
    url(r'^delete/(?P<pk>\d+)/$', views.LobbyDeleteView.as_view(), name='delete')
]
