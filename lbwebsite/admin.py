from django.contrib import admin

from .models import DiscordGuild, GuildCustomCommand, GuildPrefix, GuildServer, Character, RealmConnected


class CharacterAdmin(admin.ModelAdmin):
    def get_main_guild(self, obj):
        return " |".join([r.name for r in obj.main_for_guild.all()])
    list_display = ('user', 'region', 'server_slug', 'name', 'get_main_guild')


class GuildAdmin(admin.ModelAdmin):
    list_display = ('guild_id', 'name')

class RealmConnectedAdmin(admin.ModelAdmin):

    def get_connected_realms(self, obj):
        return " | ".join([r.server_slug for r in obj.connected_realm.all()])

    list_display = ('region', 'server_slug', 'get_connected_realms')
    search_fields = ('server_slug', )


admin.site.register(DiscordGuild, GuildAdmin)
admin.site.register(GuildCustomCommand)
admin.site.register(GuildPrefix)
admin.site.register(GuildServer)
admin.site.register(Character, CharacterAdmin)
admin.site.register(RealmConnected, RealmConnectedAdmin)
