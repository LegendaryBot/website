from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import user_passes_test, login_required
from django.shortcuts import render, redirect

from lbwebsite.forms import PrefixForm
from lbwebsite.models import Guild, GuildPrefix
from . import context_processors

def is_server_admin(request,id):
    if request.user.is_superuser:
        return True
    servers = context_processors.get_discord_servers(request)
    for server in servers['servers']:
        if server['id'] == id:
            return True
    return False


def index(request):
    return render(request, 'lbwebsite/index.html')


def logout_view(request):
    logout(request)
    return redirect('index')

@login_required
def server(request, guild_id):
    if not is_server_admin(request, guild_id):
        return redirect('index')
    try:
        guild = Guild.objects.get(pk=guild_id)
    except Guild.DoesNotExist:
        guild = Guild(guild_id=guild_id)
        guild.save()
    return render(request, 'lbwebsite/server.html', {'guild': guild, 'prefix_form': PrefixForm()})


def server_prefix_post(request, guild_id):
    if not is_server_admin(request, guild_id):
        return redirect('/')
    if not request.POST:
        return redirect('server', guild_id=guild_id)
    form = PrefixForm(request.POST)
    if form.is_valid():
        guild = Guild.objects.get(pk=guild_id)
        prefix = GuildPrefix(prefix=form.cleaned_data['prefix'], guild=guild)
        prefix.save()
        messages.add_message(request, messages.SUCCESS, f'Prefix {prefix.prefix} added to the server!')
    else:
        messages.add_message(request, messages.ERROR, 'Prefix is invalid')
    return redirect('server', guild_id=guild_id)


def server_remove_prefix(request, guild_id, prefix):
    if not is_server_admin(request, guild_id):
        return redirect('/')
    prefix = GuildPrefix.objects.filter(prefix=prefix, guild_id=guild_id).first()
    if prefix:
        prefix.delete()
        messages.add_message(request, messages.SUCCESS, f'Prefix {prefix} removed from the server!')
    return redirect('server', guild_id=guild_id)

@login_required
def myself(request):
    social = request.user.social_auth
    return render(request, 'lbwebsite/myself.html')