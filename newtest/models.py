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


    def update(self, token):
        self.access_token=token['access_token']
        self.refresh_token=token['refresh_token']
        self.expires=token['expires']

    def as_dict(self):
        d={'access_token': self.access_token,
               'refresh_token': self.refresh_token,
               'expires': self.expires,}
        return d


    @classmethod
    def from_dict(cls,user,token):
        tkn=cls(user=user, access_token=token['access_token'], refresh_token=token['refresh_token'], expires=token['expires'])
        return tkn

class EmailTemplates(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    body_template = models.TextField(verbose_name='email message template',
                                                default='Happy Birthday {{Name}}!, from {{Doctor}}.')

    subject_template = models.CharField(verbose_name='email subject template',
                                                                 max_length=100, 
                                                                 default='Happy Birthday!')