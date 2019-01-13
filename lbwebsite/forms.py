from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from slugify import slugify

from lbwebsite.models import GuildServer, GuildRank
from lbwebsite.utils import execute_battlenet_request


class PrefixForm(forms.Form):
    prefix = forms.CharField(max_length=10, label='Prefix', min_length=1)


class GuildServerForm(ModelForm):
    class Meta:
        model = GuildServer
        fields = ['region', 'server_slug', 'guild_name']

    def clean(self):
        # We check if the server & guild exists.
        self.cleaned_data['server_slug'] = slugify(self.cleaned_data['server_slug'])
        r = execute_battlenet_request(f"https://{dict(GuildServer.choices)[self.cleaned_data['region']]}.api.blizzard.com/wow/guild/{self.cleaned_data['server_slug']}/{self.cleaned_data['guild_name']}")
        if not r.ok:
            raise ValidationError('Guild not found on the realm!')
        return self.cleaned_data


class GuildRankForm(ModelForm):
    class Meta:
        model = GuildRank
        fields = ['wow_guild', 'rank_id', 'discord_rank']

    def __init__(self, guild, *args, **kwargs):
        super (GuildRankForm,self ).__init__(*args,**kwargs)
        self.fields['wow_guild'].queryset = GuildServer.objects.filter(guild=guild)