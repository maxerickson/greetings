Greetings emails birthday greetings to patients at a drchrono practice.
Greetings connects to the drcrono API using OAuth2, pulling data from 
the API as needed and then sends the messages using Django's built
in email package.

Messages can be customized and it is easy to temporarily pause the
messages.

To install greetings, install the dependencies and then add greetings
to a Django site. Then add a daily cron job that runs the sendgreetings
command that greetings adds to Django. With no options, the command
generates birthday messages for the day it is run:

    python manage.py sendgreetings

This command can also be used directly to trigger sending messages
for a given day:

    python manage.py sendgreetings --date 2016-01-01

Dependencies
----------------------
Greetings has several dependencies, including Django itself:

Django, django-bootstrap3, requests, oauthlib, requests-oauthlib and 
pytz

These can be installed using pip:

    pip -r requirements.txt

Configuration
----------------------
Add greetings' urls to the site urls.py, for example:

    urlpatterns = [
        url(r'^admin/', admin.site.urls),
        url(r'', include('greetings.urls')),
    ]

Add greetings and django-bootstrap 3 to installed apps in 
settyings.py

    INSTALLED_APPS = [
        'greetings.apps.GreetingsConfig',
        'bootstrap3',
        ...
    ]

The OAuth2 configuration for Greetings is pulled from the django site
settings.py file. Two settings are specific to each install of the app and 
must be obtained from drchrono:

    GREETINGS_OAUTH_CLIENT_ID = r'from drchrono app registration'
    GREETINGS_OAUTH_CLIENT_SECRET = r'from drchrono app registration'

The rest of the settings are standard, but it may be useful to use different
settings for testing:

    GREETINGS_OAUTH_AUTHORIZATION_URL = 'https://drchrono.com/o/authorize'
    GREETINGS_OAUTH_TOKEN_URL = 'https://drchrono.com/o/token'
    GREETINGS_OAUTH_SCOPE = ['user:read', 'patients:summary:read']

Users are authenticated against Django's RemoteUserBackend, so add it to
AUTHENTICATION_BACKENDS, something like:

    AUTHENTICATION_BACKENDS = (
        'django.contrib.auth.backends.ModelBackend',
        'django.contrib.auth.backends.RemoteUserBackend',
    )

The templates use django-bootstrap3 and Bootstrap, so Bootstrap themes
can be used to change the look of the site, for example:

    BOOTSTRAP3 = {
    'theme_url': "https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap-theme.min.css"
    }

Django sends emails using it's built in smtp backend. To choose
A different backend, configure EMAIL_BACKEND:

    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

Consult the DJango documentation for further information about configuring the
SMTP backend

    https://docs.djangoproject.com/en/1.9/topics/email/#smtp-backend


Notes
---------

requests-oauthlib will raise an error when it is not used over a secure
connection. For development and testing, this behavior can be
disabled with an environment variable:

    export OAUTHLIB_INSECURE_TRANSPORT=1

