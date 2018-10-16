from django.contrib import admin

from .models import DiscordGuild, GuildCustomCommand, GuildPrefix, GuildServer, Character, RealmConnected, GuildRank, \
    GuildSetting


class CharacterAdmin(admin.ModelAdmin):
    def get_main_guild(self, obj):
        return " |".join([r.name for r in obj.main_for_guild.all()])
    list_display = ('user', 'region', 'server_slug', 'name', 'get_main_guild')
    search_fields = ('user__username', 'name', 'main_for_guild__name')


class GuildAdmin(admin.ModelAdmin):
    list_display = ('guild_id', 'name')
    search_fields = ('guild_id', 'name')


class RealmConnectedAdmin(admin.ModelAdmin):

    def get_connected_realms(self, obj):
        return " | ".join([r.server_slug for r in obj.connected_realm.all()])

    list_display = ('region', 'server_slug', 'get_connected_realms')
    search_fields = ('server_slug', )

class GuildPrefixAdmin(admin.ModelAdmin):
    list_display = ('guild', 'prefix')
    search_fields = ('guild__name', 'guild__guild_id', 'prefix')

class GuildRankAdmin(admin.ModelAdmin):
    list_display = ('guild','rank_id', 'discord_rank')
    search_fields = ('guild__name', 'guild__guild_id', 'rank_id', 'discord_rank')

class GuildCustomCommandAdmin(admin.ModelAdmin):
    list_display = ('guild', 'name', 'type', 'value')
    search_fields = ('guild__name', 'guild__guild_id', 'name')

class GuildSettingAdmin(admin.ModelAdmin):
    list_display = ('guild', 'setting_name', 'setting_value')
    search_fields = ('guild__name', 'guild__guild_id', 'setting_name')

class GuildServerAdmin(admin.ModelAdmin):
    list_display = ('guild', 'region', 'server_slug', 'guild_name', 'default')
    search_fields = ('guild__name', 'guild__guild_id', 'region', 'server_slug', 'guild_name')

admin.site.register(DiscordGuild, GuildAdmin)
admin.site.register(GuildCustomCommand, GuildCustomCommandAdmin)
admin.site.register(GuildPrefix, GuildPrefixAdmin)
admin.site.register(GuildServer, GuildServerAdmin)
admin.site.register(Character, CharacterAdmin)
admin.site.register(RealmConnected, RealmConnectedAdmin)
admin.site.register(GuildRank, GuildRankAdmin)
admin.site.register(GuildSetting, GuildSettingAdmin)
