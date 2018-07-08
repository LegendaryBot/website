from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('logout', views.logout_view, name='logout'),
    re_path(r'^server/(?P<guild_id>[0-9]+)$', views.server, name='server'),
    re_path(r'^server/(?P<guild_id>[0-9]+)/prefix$', views.server_prefix_post, name='server_prefix'),
    re_path(r'^server/(?P<guild_id>[0-9]+)/(?P<prefix>.*)$', views.server_remove_prefix, name='server_remove_prefix'),
    path('myself', views.myself, name='myself'),
    path('myself/character/<int:character_id>', views.myself_update, name='update_character')
]