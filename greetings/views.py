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

from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.forms.models import model_to_dict

from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone

import datetime

from django.conf import settings
from .models import Token, EmailTemplates
from .forms import EmailTemplatesForm
#~ from .utils import get_patients, oauth_session
from .utils import ChronoHandler, oauth_session

def home(request):
    if request.user.is_authenticated():
        handler=ChronoHandler(request.user)
        patients = handler.get_patients()#birthday=datetime.date.today())
        doctors = handler.doctor_map()
        for p in patients:
            p['doctor_name'] = doctors[p['doctor']]
        username = request.user.get_username()
        context = {'username': username, 'patient_list': patients}
        return render(request, 'greetings/index.html', context)
    return render(request, 'greetings/splash.html')

def register(request):
    oauth = oauth_session(callback=request.build_absolute_uri(reverse('greetings:authorize')))
    authorization_url, state = oauth.authorization_url(settings.GREETINGS_OAUTH_AUTHORIZATION_URL)
    request.session['oauth_state'] = state
    request.session.modified = True
    return redirect(authorization_url)

# handle OAuth2 callback
def authorize(request):
    # handle explicit error parameters in redirect
    if 'error' in request.GET:
        messages.error(request, 'OAuth authentication with drchrono failed.')
        return redirect('greetings:home')

    oauth = oauth_session(callback=request.build_absolute_uri(reverse('greetings:authorize')),
                        state=request.session['oauth_state'] )
    token = {}
    try:
        token = oauth.fetch_token(
            settings.GREETINGS_OAUTH_TOKEN_URL,
            code=request.GET['code'],
            #~ grant_type='authorization_code',
            #~ authorization_response=authorization_response,
            client_secret=settings.GREETINGS_OAUTH_CLIENT_SECRET)
    except:
        raise
        messages.error(request, 'Could not retrieve OAuth token from drchrono.')
    if token:
        # fetch profile to associate token with username.
        profile = oauth.get('https://drchrono.com/api/users/current').json()
        user = authenticate(remote_user=profile['username'])
        login(request, user)
        #~ # serialize token information to database for later use.
        try: # fetch and update token
            tkn = user.token
            tkn.update(token)
        except Token.DoesNotExist: # new user, create token
            tkn = Token.from_dict(user, token)
            tkn.save()
            eml = EmailTemplates(user=user)
            eml.save()
            messages.info(request, 'Welcome to Greetings!')
    return redirect('greetings:home')

def logout(request):
    auth_logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('greetings:home')

@login_required(login_url='greetings:home')
def settings_view(request):
    templatedata = request.user.emailtemplates
    # save post and reload page
    if request.method == 'POST':
        form = EmailTemplatesForm(request.POST,
                                  initial=model_to_dict(templatedata),
                                  instance=templatedata)
        if form.is_valid():
            if form.has_changed():
                form.save()
                messages.success(request, 'Acccount settings updated.')
            return redirect('greetings:settings')
    else:
        form = EmailTemplatesForm(initial=model_to_dict(templatedata))

    return render(request, 'greetings/manage.html', {'email_templates': form})

@login_required(login_url='greetings:home')
def delete(request):
    if request.method == 'POST':
        user = request.user
        auth_logout(request)
        user.delete()
        messages.success(request, 'Account information has been deleted.')
        return redirect('greetings:home')

    return render(request, 'greetings/confirm_delete.html')
