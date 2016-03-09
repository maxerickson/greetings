from django.conf import settings

from django.contrib.auth.models import User
from .models import Token

from requests_oauthlib import OAuth2Session

from django.utils import timezone
import datetime
import logging





def oauth_session(callback):
    scope=["read"]
#~ scope=["user:read","patients:summary:read"]
    return OAuth2Session(client_id = settings.OAUTH_CLIENT_ID, 
                                                redirect_uri=callback,
                                                scope=scope)


def get_patients(user, date=None):
	oauth=OAuth2Session(client_id = settings.OAUTH_CLIENT_ID, token=user.token.as_dict())
	patients = []
	#~ patients_url = 'https://drchrono.com/api/patients'
	patients_url="http://localhost:9000/patient1"
	if date is not None:
		#~ setup date query
		pass
	while patients_url:
	    data = oauth.get(patients_url).json()
	    patients.extend(data['results'])
	    patients_url = data['next']
	return patients