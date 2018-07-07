from django.contrib import admin

from .models import Guild, GuildCustomCommand, GuildPrefix, GuildServer, Character

# Register your models here.

class CharacterAdmin(admin.ModelAdmin):
    list_display = ('user', 'region', 'server_slug', 'name')

admin.site.register(Guild)
admin.site.register(GuildCustomCommand)
admin.site.register(GuildPrefix)
admin.site.register(GuildServer)
admin.site.register(Character, CharacterAdmin)
