

The OAuth2 configuration for Greetings is pulled from the django site
settings file. Two settings are specific to each install of the app and 
must be obtained from Dr Chrono:

GREETINGS_OAUTH_CLIENT_ID = r'from Dr Chrono app registration'
GREETINGS_OAUTH_CLIENT_SECRET = r'from Dr Chrono app registration'

The rest of the settings are standard, but it may be useful to use different
settings for testing:

    GREETINGS_OAUTH_AUTHORIZATION_URL = 'https://drchrono.com/o/authorize'
    GREETINGS_OAUTH_TOKEN_URL = 'https://drchrono.com/o/token'
    GREETINGS_OAUTH_SCOPE = ['user:read', 'patients:summary:read']
    GREETINGS_PATIENTS_URL = 'https://drchrono.com/api/patients'
    GREETINGS_PROFILE_URL = 'https://drchrono.com/api/users/current'

Configure a theme for bootstrap3, for example:

    BOOTSTRAP3 = {
    'theme_url': "https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap-theme.min.css"
    }