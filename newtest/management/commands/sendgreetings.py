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

from django.core.management.base import BaseCommand, CommandError

from django.core.mail import send_mail
import smtplib

from django.contrib.auth.models import User
from newtest.models import Token
import newtest.utils

import logging
logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Generate and send birthday greetings.'

    def handle(self, *args, **options):
        self.stdout.write("Hello Command")
        for user in User.objects.all():
            try:
                patients=newtest.utils.get_patients(user)
            except Token.DoesNotExist:
                # admin and staff users might not have tokens
                pass
            else:
                for patient in patients:
                    body=self.fill("Happy Birthday {{Name}}!, from {{Doctor}}.", patient)
                    self.send("Happy Birthday!", body,
                                "from2@example.com", ["to@example.com"])

    def fill(self, template, patient):
        templ="Happy Birthday {{Name}}!, from {{Doctor}}."
        body=template.replace('{{Name}}', patient['first_name'] + ' ' + patient['last_name'])
        body=body.replace('{{Doctor}}', patient['doctor'])
        return body


    def send(self, subject, body, sender, recipients):
        try:
                send_mail(subject, body, sender,
                                recipients, fail_silently=False)
        except smtplib.SMTPException:
                logger.warning('Message to %s failed' % self.dest)
        else:
                # update last sent message
                pass