import requests
from django.core.cache import cache

from lbwebsite.Permissions import Permissions


def get_discord_servers_admin(request):
    if request.user.is_authenticated:
        if 'admin' in request.META['PATH_INFO']:
            return {}
        if cache.get(f"discord_cache:{request.user.id}"):
            return {'servers_admin': cache.get(f"discord_admin_cache:{request.user.id}"), 'servers': cache.get(f"discord_cache:{request.user.id}")}
        social = request.user.social_auth.get(provider='discord')
        response = requests.get('https://discordapp.com/api/v6/users/@me/guilds', headers={'Authorization':f"Bearer {social.extra_data['access_token']}"})
        if response.ok:
            admin_servers = []
            servers = []
            json_value = response.json()
            for server in json_value:
                perm = Permissions(server['permissions'])
                if perm.administrator:
                    admin_servers.append({"id": int(server['id']), "name":server['name']})
                servers.append({"id": int(server['id']), "name":server['name']})
            cache.set(f"discord_admin_cache:{request.user.id}", admin_servers, 60*60)
            cache.set(f"discord_cache:{request.user.id}", servers, 60*60)
            return {'servers_admin': admin_servers, 'servers': servers}
    return {}