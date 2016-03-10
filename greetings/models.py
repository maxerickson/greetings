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

from django.db import models
from django.contrib.auth.models import User


class Token(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    access_token = models.BinaryField()
    refresh_token = models.BinaryField()
    expires_at = models.FloatField()

    def update(self, token):
        self.access_token = token['access_token']
        self.refresh_token = token['refresh_token']
        self.expires_at = token['expires_at']
        self.save()

    def as_dict(self):
        d = {'access_token': self.access_token,
             'refresh_token': self.refresh_token,
             'expires_at': self.expires_at,}
        return d

    @classmethod
    def from_dict(cls, user, token):
        tkn = cls(user=user,
                  access_token=token['access_token'],
                  refresh_token=token['refresh_token'],
                  expires_at=token['expires_at'])
        return tkn

class EmailTemplates(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    body_template = models.TextField(verbose_name='email message template',
                                     default='Happy Birthday {{Name}}!, from {{Doctor}}.')

    subject_template = models.CharField(verbose_name='email subject template',
                                        max_length=100,
                                        default='Happy Birthday!')

    send_messages = models.BooleanField(verbose_name='Send Messages', default=True)
