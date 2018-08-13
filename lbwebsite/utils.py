from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
from django.conf import settings


def get_battlenet_oauth(region: str):
    if region.upper() == 'US':
        client_id = settings.SOCIAL_AUTH_BATTLENET_OAUTH2_US_KEY
        client_secret = settings.SOCIAL_AUTH_BATTLENET_OAUTH2_US_SECRET
    else:
        client_id = settings.EU_KEY
        client_secret = settings.EU_SECRET
    client = BackendApplicationClient(client_id=client_id)
    oauth = OAuth2Session(client=client)
    oauth.fetch_token(token_url=f"https://{region}.battle.net/oauth/token", client_id=client_id, client_secret=client_secret)
    return oauth
