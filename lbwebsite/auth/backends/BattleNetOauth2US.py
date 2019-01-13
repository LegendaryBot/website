from social_core.backends.oauth import BaseOAuth2


class BattleNetOAuth2US(BaseOAuth2):
    """ battle.net Oauth2 backend"""
    name = 'battlenet-oauth2-us'
    ID_KEY = 'id'
    REDIRECT_STATE = False
    AUTHORIZATION_URL = 'https://us.battle.net/oauth/authorize'
    ACCESS_TOKEN_URL = 'https://us.battle.net/oauth/token'
    ACCESS_TOKEN_METHOD = 'POST'
    REVOKE_TOKEN_METHOD = 'GET'
    DEFAULT_SCOPE = ['wow.profile']
    EXTRA_DATA = [
        ('refresh_token', 'refresh_token', True),
        ('expires_in', 'expires'),
        ('token_type', 'token_type', True)
    ]

    def get_characters(self, access_token):
        """
        Fetches the character list from the battle.net API. Returns list of
        characters or empty list if the request fails.
        """
        params = {'access_token': access_token}
        if self.setting('API_LOCALE'):
            params['locale'] = self.setting('API_LOCALE')

        response = self.get_json(
            'https://us.api.blizzard.com/wow/user/characters',
            params=params
        )
        return response.get('characters') or []

    def get_user_details(self, response):
        """ Return user details from Battle.net account """
        return {'battletag': response.get('battletag')}

    def user_data(self, access_token, *args, **kwargs):
        """ Loads user data from service """
        return self.get_json(
            'https://us.api.battle.net/oauth/userinfo',
            params={'access_token': access_token}
        )