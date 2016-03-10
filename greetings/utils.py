#   Copyright 2016 Max Erickson
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

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
    while patients_url:
        data = oauth.get(patients_url).json()
        #~ print data
        patients.extend(data['results'])
        patients_url = data['next']
    if birthday is not None:
        monthday=birthday.isoformat()[5:].decode()
        tokeep=list()
        for p in patients:
            dob=p['date_of_birth']
            if dob is not None and dob[5:]==monthday:
                tokeep.append(p)
            elif dob:
                print dob[5:], monthday
        patients=tokeep
    return patients
