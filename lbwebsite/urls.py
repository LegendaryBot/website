from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('logout', views.logout_view, name='logout'),
    re_path(r'^server/(?P<guild_id>[0-9]+)$', views.server, name='server'),
    re_path(r'^server/(?P<guild_id>[0-9]+)/prefix$', views.server_prefix_post, name='server_prefix'),
    re_path(r'^server/(?P<guild_id>[0-9]+)/prefix/(?P<prefix>.*)$', views.server_remove_prefix, name='server_remove_prefix'),
    re_path(r'^server/(?P<guild_id>[0-9]+)/command/(?P<command_name>.*)$', views.server_remove_custom_command, name='server_remove_custom_command'),
    re_path(r'^server/(?P<guild_id>[0-9]+)/guild$', views.server_add_guild_server, name='server_add_guild_server'),
    re_path(r'^server/(?P<guild_id>[0-9]+)/guild/(?P<guild_server_id>.*)$', views.server_make_default_guild_server, name='server_default_guild_server'),
    path('update_realm', views.update_realm, name="update_realm"),
    path('myself', views.myself, name='myself'),
    path('myself/character/<int:character_id>', views.myself_update, name='update_character')
]