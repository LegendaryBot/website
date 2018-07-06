from django.contrib import admin

from .models import Guild, GuildCustomCommands, GuildPrefix, GuildServers
# Register your models here.
admin.site.register(Guild)
admin.site.register(GuildCustomCommands)
admin.site.register(GuildPrefix)
admin.site.register(GuildServers)
