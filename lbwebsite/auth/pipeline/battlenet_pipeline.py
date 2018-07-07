from slugify import slugify

from lbwebsite.models import Character


def save_characters(backend, user, response, *args, **kwargs):
    if backend.name == 'battlenet-oauth2-us' or backend.name == 'battlenet-oauth2-eu':
        characters = backend.get_characters(response.get('access_token'))
        region = backend.name.split('-')[2]
        region_int = [x for x,y in Character.choices if y == region.upper()][0]
        user_characters = Character.objects.filter(user=user, region=region_int).all()
        for character in user_characters:
            exist = False
            for bnet_character in characters:
                realm_slug = slugify(bnet_character['realm'])
                if character.region == region and character.server_slug == realm_slug and character.name == bnet_character['name']:
                    exist = True
            if not exist:
                character.delete()
        for character in characters:
            realm_slug = slugify(character['realm'])

            character_database = Character.objects.filter(region=region_int, server_slug=realm_slug, name=character['name']).first()
            if not character_database:
                character_database = Character(region=region_int, server_slug=realm_slug, name=character['name'], user=user)
            character_database.thumbnail = character['thumbnail']
            if 'guild' in character:
                character_database.guild_name = character['guild']
            else:
                character_database.guild_name = None
            character_database.save()