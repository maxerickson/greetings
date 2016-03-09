from django.db import models

from django.contrib.auth.models import User

from django.utils import timezone
import datetime

from requests_oauthlib import OAuth2Session



def _oath_handler(request):
    scope=["read"]
    #~ scope=["user:read","patients:summary:read"]
    handler=OAuth2Session(client_id = settings.OAUTH_CLIENT_ID, 
                                            redirect_uri=request.build_absolute_uri(reverse('greetings:authorize')),
                                            scope=scope)
    return handler

class Token(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    access_token = models.BinaryField()
    refresh_token = models.BinaryField()
    expires = models.DateTimeField()
    #timezone.now() + datetime.timedelta(seconds=data['expires_in'])


    def refresh():
        pass