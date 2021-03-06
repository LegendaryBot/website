from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from lbwebsite.decorators import is_server_admin
from lbwebsite.forms import PrefixForm, GuildServerForm, GuildRankForm
from lbwebsite.models import DiscordGuild, GuildPrefix, Character, GuildCustomCommand, GuildServer, RealmConnected, \
    GuildRank
from lbwebsite.utils import execute_battlenet_request


def index(request):
    return render(request, 'lbwebsite/index.html')


def logout_view(request):
    logout(request)
    return redirect('index')


@login_required
@is_server_admin
def server(request, guild_id):
    try:
        guild = DiscordGuild.objects.get(pk=guild_id)
    except DiscordGuild.DoesNotExist:
        guild = DiscordGuild(guild_id=guild_id)
        guild.save()
    return render(request, 'lbwebsite/server.html', {'guild': guild, 'prefix_form': PrefixForm(), 'guild_server_form': GuildServerForm(), 'guild_rank_form': GuildRankForm(guild)})


@login_required
@require_POST
@is_server_admin
def server_prefix_post(request, guild_id):
    form = PrefixForm(request.POST)
    if form.is_valid():
        guild = DiscordGuild.objects.get(pk=guild_id)
        prefix = GuildPrefix(prefix=form.cleaned_data['prefix'], guild=guild)
        prefix.save()
        messages.add_message(request, messages.SUCCESS, f'Prefix {prefix.prefix} added to the server!')
    else:
        messages.add_message(request, messages.ERROR, 'Prefix is invalid')
    return redirect('server', guild_id=guild_id)


@login_required
@is_server_admin
def server_remove_prefix(request, guild_id, prefix):
    prefix = GuildPrefix.objects.filter(prefix=prefix, guild_id=guild_id).first()
    if prefix:
        prefix.delete()
        messages.add_message(request, messages.SUCCESS, f'Prefix {prefix} removed from the server!')
    return redirect('server', guild_id=guild_id)


@login_required
@is_server_admin
def server_remove_custom_command(request, guild_id, command_name):
    custom_command = GuildCustomCommand.objects.filter(guild_id=guild_id, name=command_name).first()
    if custom_command:
        custom_command.delete()
        messages.add_message(request, messages.SUCCESS, f"Command {command_name} removed!")
    else:
        messages.add_message(request, messages.ERROR, f"Command {command_name} not found!")
    return redirect('server', guild_id=guild_id)


@login_required
@require_POST
@is_server_admin
def server_add_guild_server(request, guild_id):
    form = GuildServerForm(request.POST)
    if form.is_valid():
        guild_server = form.save(commit=False)
        try:
            GuildServer.objects.get(guild_id=guild_id, default=True)
        except GuildServer.DoesNotExist:
            guild_server.default = True
        guild_server.guild = DiscordGuild.objects.get(pk=guild_id)
        guild_server.save()
        messages.add_message(request, messages.SUCCESS, 'Server added!')
    else:
        messages.add_message(request, messages.ERROR, 'The Server is invalid!')
    return redirect('server', guild_id=guild_id)


@login_required
@is_server_admin
def server_make_default_guild_server(request, guild_id, guild_server_id):
    try:
        guild_server = GuildServer.objects.get(guild_id=guild_id, pk=guild_server_id)

        guild_server_default = GuildServer.objects.get(guild_id=guild_id, default=True)
        guild_server_default.default = False
        guild_server_default.save()
        guild_server.default = True
        guild_server.save()
        messages.add_message(request, messages.SUCCESS, 'The server has been set as the default one!')
    except GuildServer.DoesNotExist:
        messages.add_message(request, messages.ERROR, 'The server you want to set as default does not exist!')
    return redirect('server', guild_id=guild_id)


@login_required
def myself(request):
    return render(request, 'lbwebsite/myself.html')


@login_required
def myself_update(request, character_id):
    if request.POST and request.user.is_authenticated:
        selected_servers = request.POST.getlist('servers')
        character = Character.objects.get(pk=character_id)
        if character.user == request.user:
            character.main_for_guild.clear()
            if selected_servers:
                for server in selected_servers:
                    guild = DiscordGuild.objects.get(pk=server)
                    if guild:
                        character.main_for_guild.add(guild)
                        character.save()
        messages.add_message(request, messages.SUCCESS, f'Character {character.name} modified successfully.')
    return redirect('myself')


@is_server_admin
@login_required
def server_remove_guild_server(request,guild_id, guild_server_id):
    guild_server = GuildServer.objects.get(guild_id=guild_id, pk=guild_server_id)
    guild_server.delete()
    if guild_server.default:
        guild_server_new_default = GuildServer.objects.filter(guild_id=guild_id).first()
        if guild_server_new_default:
            guild_server_new_default.default = True
            guild_server_new_default.save()
            messages.add_message(request, messages.SUCCESS, f"Guild removed. Guild {guild_server_new_default.guild_name} set as default.")
        else:
            messages.add_message(request, messages.SUCCESS, "Guild removed!")
    else:
        messages.add_message(request, messages.SUCCESS, f"Guild removed.")
    return redirect('server', guild_id=guild_id)


@login_required
@require_POST
@is_server_admin
def server_add_rank(request, guild_id):
    form = GuildRankForm(DiscordGuild.objects.get(pk=guild_id), request.POST)
    if form.is_valid():
        guild_rank = form.save(commit=False)
        if guild_rank.wow_guild.guild.guild_id == int(guild_id):
            guild_rank.guild = DiscordGuild.objects.get(pk=guild_id)
            guild_rank.save()
            messages.add_message(request, messages.SUCCESS, f"Rank added!")
        else:
            messages.add_message(request, messages.ERROR, f"This Guild doesn't exist! Please select a valid guild")
    else:
        messages.add_message(request, messages.ERROR, "Error in the rank form. Please fix the errors.")
    return redirect('server', guild_id=guild_id)


@login_required
@is_server_admin
def server_remove_rank(request, guild_id, rank_id):
    guild_rank = GuildRank.objects.get(pk=rank_id, guild_id=guild_id)
    guild_rank.delete()
    messages.add_message(request, messages.SUCCESS, f"Rank removed!")
    return redirect('server', guild_id=guild_id)

@login_required
@staff_member_required
def update_realm(request, region):
    params = {
        "locale": "en_US",
        "namespace": f"dynamic-{region}"
    }
    result = execute_battlenet_request(f"https://{region}.api.blizzard.com/data/wow/connected-realm/", params=params)
    if result.ok:
        RealmConnected.objects.filter(region=1 if region.upper() == "US" else 2).all().delete()
        connected_realms_json = result.json()
        for realm_entry in connected_realms_json['connected_realms']:
            connected_realm_entry_bnet = execute_battlenet_request(realm_entry['href'])
            realms = []
            if connected_realm_entry_bnet.ok:
                connected_realm_entry_json = connected_realm_entry_bnet.json()
                for connected_realm_entry in connected_realm_entry_json['realms']:
                    realm_database_entry = RealmConnected()
                    realm_database_entry.region = 1 if region.upper() == "US" else 2
                    realm_database_entry.server_slug = connected_realm_entry['slug']
                    realm_database_entry.save()
                    for realm in realms:
                        realm_database_entry.connected_realm.add(realm)
                        realm_database_entry.save()
                    realms.append(realm_database_entry)
    return HttpResponse("Done!")
