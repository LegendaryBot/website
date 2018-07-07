import requests

from lbwebsite.Permissions import Permissions


def get_discord_servers(request):
    if request.user.is_authenticated:
        social = request.user.social_auth.get(provider='discord')
        response = requests.get('https://discordapp.com/api/v6/users/@me/guilds', headers={'Authorization':f"Bearer {social.extra_data['access_token']}"})
        servers = []
        json_value = response.json()
        for server in json_value:
            perm = Permissions(server['permissions'])
            if perm.administrator:
                servers.append({"id": int(server['id']), "name":server['name']})
        return {'servers': servers}
    return {}