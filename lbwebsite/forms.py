from django import forms


class PrefixForm(forms.Form):
    prefix = forms.CharField(max_length=10, label='Prefix', min_length=1)