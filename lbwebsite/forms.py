import requests
from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.conf import settings
from slugify import slugify

from lbwebsite.models import GuildServer


class PrefixForm(forms.Form):
    prefix = forms.CharField(max_length=10, label='Prefix', min_length=1)


class GuildServerForm(ModelForm):
    class Meta:
        model = GuildServer
        fields = ['region', 'server_slug', 'guild_name']

    def clean(self):
        # We check if the server & guild exists.
        self.cleaned_data['server_slug'] = slugify(self.cleaned_data['server_slug'])
        r = requests.get(f"https://{dict(GuildServer.choices)[self.cleaned_data['region']]}.api.battle.net/wow/guild/{self.cleaned_data['server_slug']}/{self.cleaned_data['guild_name']}", params={"apikey": settings.SOCIAL_AUTH_BATTLENET_OAUTH2_US_KEY})
        if not r.ok:
            raise ValidationError('Guild not found on the realm!')
        return self.cleaned_data
