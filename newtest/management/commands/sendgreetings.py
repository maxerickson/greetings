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

from django.template import Context, Template
from django.core.mail import send_mail
import smtplib

from django.utils import timezone
import datetime

from django.contrib.auth.models import User
from newtest.models import Token

import newtest.utils

import logging
logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Generate and send birthday greetings.'

    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument('--date',
            action='store',
            dest='date',
            default=None,
            help='Date to send birthday greetings for, numeric month and day.')

    def handle(self, *args, **options):
        today=timezone.now().date()
        if options['date']:
            try:
                m,d=options['date'].split('-')
                date=datetime.date(today.year, int(m), int(d))
            except:
                import sys
                sys.stdout.write('Error parsing date fragment. Use numbers for month and day. Omit year.\n')
                sys.exit(1)
        else:
            date=today
        for user in User.objects.all():
            try:
                patients=newtest.utils.get_patients(user, date=date)
            except Token.DoesNotExist:
                # admin and staff users might not have tokens
                pass
            else:
                subject_template=Template(user.emailtemplates.subject_template)
                body_template=Template(user.emailtemplates.body_template)
                for patient in patients:
                    context=Context({'Name': patient['first_name'] + ' ' + patient['last_name'],
                              'FirstName': patient['first_name'],
                              'LastName': patient['last_name'],
                              'Doctor': patient['doctor']})
                    self.send(subject_template.render(context), body_template.render(context),
                                "no-reply@example.com", [patient['email']])

    def send(self, subject, body, sender, recipients):
        try:
                send_mail(subject, body, sender,
                                recipients, fail_silently=False)
        except smtplib.SMTPException:
                logger.warning('Message to %s failed' % self.dest)
        else:
                # todo: track sent messages
                pass