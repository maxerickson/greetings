import requests_oauthlib
from django.conf import settings

from django.contrib.auth.models import User
from .models import Token

from django.utils import timezone
import datetime
import logging


def oauth_session(callback):
    scope=["read"]
#~ scope=["user:read","patients:summary:read"]
    return requests_oauthlib.OAuth2Session(client_id = settings.OAUTH_CLIENT_ID, 
                                                redirect_uri=callback,
                                                scope=scope)


def get_patients(user):
	oauth=requests_oauthlib.OAuth2Session(access_token=user.token['access_token'])
	patients = []
	#~ patients_url = 'https://drchrono.com/api/patients'
	patients_url="http://localhost:9000/patient1"
	while patients_url:
	    data = oauth.get(patients_url, headers=headers).json()
	    patients.extend(data['results'])
	    patients_url = data['next']
	return patients