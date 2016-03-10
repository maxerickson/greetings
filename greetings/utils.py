from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings

import datetime
from requests_oauthlib import OAuth2Session


def oauth_session(callback):
    """Returns OAuth2 session with prefilled client info."""
    scope = settings.GREETINGS_OAUTH_SCOPE
    return OAuth2Session(client_id=settings.GREETINGS_OAUTH_CLIENT_ID,
                         redirect_uri=callback,
                         scope=scope)

def get_patients(user, birthday=None):
    """Returns patients associated with a user."""
    oauth = OAuth2Session(client_id=settings.GREETINGS_OAUTH_CLIENT_ID,
                          token=user.token.as_dict(),
                          # if the existing Bearer token is expired, requests_oathlib
                          # will automatically fetch a new token and pass it 
                          # to the token_updater. The update method on Token self saves.
                          auto_refresh_url=settings.GREETINGS_OAUTH_TOKEN_URL,
                          token_updater=user.token.update)
    patients = []
    patients_url = settings.GREETINGS_PATIENTS_URL
    if birthday is not None:
        #~ setup date query
        pass
    while patients_url:
        data = oauth.get(patients_url).json()
        patients.extend(data['results'])
        patients_url = data['next']
    return patients
