from django.db import models


class Guild(models.Model):
    guild_id = models.IntegerField(primary_key=True)


class GuildPrefix(models.Model):
    guild = models.ForeignKey(Guild, on_delete=models.CASCADE)
    prefix = models.CharField(max_length=10)


class GuildCustomCommands(models.Model):
    guild = models.ForeignKey(Guild, on_delete=models.CASCADE)

    TEXT = 1

    choices = (
        (TEXT, "Text"),
    )
    type = models.IntegerField(choices=choices, default=TEXT)
    value = models.CharField(max_length=2000)


class GuildServers(models.Model):
    guild = models.ForeignKey(Guild, on_delete=models.CASCADE)

    US = 1,
    EU = 2,
    TW = 3,
    KR = 4

    choices = (
        (US, "US"),
        (EU, "EU"),
        (TW, "TW"),
        (KR, "KR")
    )
    region = models.IntegerField(choices=choices, default=US)
    server_slug = models.CharField(max_length=50)
    guild_name = models.CharField(max_length=50, null=True)
    default = models.BooleanField(default=False)