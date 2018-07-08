import requests

from lbwebsite.models import DiscordGuild


def update_guild_name(backend, user, response, *args, **kwargs):
    if backend.name == 'discord':
        response = requests.get('https://discordapp.com/api/v6/users/@me/guilds', headers={'Authorization':f"Bearer {response.get('access_token')}"})
        servers = []
        json_value = response.json()
        for server in json_value:
            try:
                guild = DiscordGuild.objects.get(pk=server['id'])
            except DiscordGuild.DoesNotExist:
                guild = DiscordGuild(pk=server['id'])
            guild.name = server['name']
            guild.save()