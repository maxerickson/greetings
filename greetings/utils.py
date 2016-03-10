from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings

import datetime
from requests_oauthlib import OAuth2Session


def oauth_session(callback, state=None):
    """Returns OAuth2 session with prefilled client info."""
    return OAuth2Session(client_id=settings.GREETINGS_OAUTH_CLIENT_ID,
                         redirect_uri=callback,
                         scope=settings.GREETINGS_OAUTH_SCOPE,
                         state=state)

def get_patients(user, birthday=None):
    """Returns patients associated with a user."""
    oauth = OAuth2Session(client_id=settings.GREETINGS_OAUTH_CLIENT_ID,
                          token=user.token.as_dict(),
                          # if the existing Bearer token is expired, requests_oathlib
                          # will automatically fetch a new token and pass it 
                          # to the token_updater. The update method on Token self saves.
                          auto_refresh_kwargs={'grant_type': 'refresh_token'},
                          auto_refresh_url=settings.GREETINGS_OAUTH_TOKEN_URL,
                          token_updater=user.token.update)
    patients = []
    patients_url = settings.GREETINGS_PATIENTS_URL
    payload={}
    if birthday is not None:
        payload['date_of_birth']=birthday.isoformat()
    while patients_url:
        data = oauth.get(patients_url, params=payload).json()
        print data
        patients.extend(data['results'])
        patients_url = data['next']
    return patients
