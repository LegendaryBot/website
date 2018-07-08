from django.contrib import admin

from .models import DiscordGuild, GuildCustomCommand, GuildPrefix, GuildServer, Character


class CharacterAdmin(admin.ModelAdmin):
    list_display = ('user', 'region', 'server_slug', 'name')


class GuildAdmin(admin.ModelAdmin):
    list_display = ('guild_id', 'name')


admin.site.register(DiscordGuild, GuildAdmin)
admin.site.register(GuildCustomCommand)
admin.site.register(GuildPrefix)
admin.site.register(GuildServer)
admin.site.register(Character, CharacterAdmin)
