from django.contrib.auth.models import User
from django.db import models, IntegrityError
from django.db.models.signals import m2m_changed
from django.dispatch import receiver


class DiscordGuild(models.Model):
    guild_id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.name} | {self.guild_id}"


class GuildPrefix(models.Model):
    guild = models.ForeignKey(DiscordGuild, on_delete=models.CASCADE)
    prefix = models.CharField(max_length=10)
    
    class Meta:
        unique_together = (('guild', 'prefix'))


class GuildCustomCommand(models.Model):
    guild = models.ForeignKey(DiscordGuild, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    TEXT = 1

    choices = (
        (TEXT, "Text"),
    )
    type = models.IntegerField(choices=choices, default=TEXT)
    value = models.CharField(max_length=2000)

    class Meta:
        unique_together = (('guild', 'name'))


class GuildServer(models.Model):
    guild = models.ForeignKey(DiscordGuild, on_delete=models.CASCADE)

    US = 1
    EU = 2
    TW = 3
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
    class Meta:
        unique_together = ("guild","region","server_slug","guild_name")

    def __str__(self):
        return f"{self.server_slug}-{self.choices[self.region - 1][1]} | {self.guild_name}"

class RealmConnected(models.Model):
    US = 1
    EU = 2
    TW = 3
    KR = 4

    choices = (
        (US, "US"),
        (EU, "EU"),
        (TW, "TW"),
        (KR, "KR")
    )
    region = models.IntegerField(choices=choices, default=US)
    server_slug = models.CharField(max_length=50)
    connected_realm = models.ManyToManyField('self')

    def __str__(self):
        return f"{self.region} - {self.server_slug}"


class Character(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    US = 1
    EU = 2
    TW = 3
    KR = 4

    choices = (
        (US, "US"),
        (EU, "EU"),
        (TW, "TW"),
        (KR, "KR"),
    )
    region = models.IntegerField(choices=choices, default=US)
    server_slug = models.CharField(max_length=50, verbose_name="Realm")
    name = models.CharField(max_length=50)
    guild_name = models.CharField(max_length=50, null=True, blank=True)
    thumbnail = models.CharField(max_length=300)
    main_for_guild = models.ManyToManyField(DiscordGuild, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.region} - {self.server_slug} - {self.name} - {self.guild_name} - {self.thumbnail}"

    def __eq__(self, other):
        if isinstance(other, Character):
            return self.region == other.region and self.server_slug == other.server_slug and self.name == other.name
        return False

    class Meta:
        unique_together = (('region', 'server_slug', 'name'))

class GuildRank(models.Model):
    guild = models.ForeignKey(DiscordGuild, on_delete=models.CASCADE)
    wow_guild = models.ForeignKey(GuildServer, on_delete=models.CASCADE)
    rank_id = models.IntegerField(verbose_name="Rank ID")
    discord_rank = models.CharField(verbose_name="Discord Rank", max_length=200)
    class Meta:
        unique_together = ("guild", "wow_guild", "rank_id")

class GuildSetting(models.Model):
    guild = models.ForeignKey(DiscordGuild, on_delete=models.CASCADE)
    setting_name = models.CharField(max_length=100)
    setting_value = models.CharField(max_length=1000)
    class Meta:
        unique_together = ("guild", "setting_name")

@receiver(m2m_changed, sender=Character.main_for_guild.through)
def verify_uniqueness_character_guild(sender, **kwargs):
    character = kwargs.get('instance', None)
    action = kwargs.get('action', None)
    guilds = kwargs.get('pk_set', None)

    if action == "pre_add":
        for guild in guilds:
            if Character.objects.filter(user=character.user).filter(main_for_guild=guild):
                raise IntegrityError('Already have a character set for this guild.')