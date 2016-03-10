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
from .utils import get_patients, oauth_session



def home(request):
    if request.user.is_authenticated():
        patients = get_patients(request.user)
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
        messages.error(request, 'OAuth authentication with Dr Chrono failed.')
        return redirect('greetings:home')

    authorization_response = request.build_absolute_uri()
    oauth = oauth_session(callback=request.build_absolute_uri(reverse('greetings:authorize')))
    token = {}
    try:
        token = oauth.fetch_token(
            settings.GREETINGS_OAUTH_TOKEN_URL,
            authorization_response=authorization_response,
            client_secret=settings.GREETINGS_OAUTH_CLIENT_SECRET)
    except:
        messages.error(request, 'Could not retrieve OAuth token from Dr Chrono.')
    if token:
        # token is valid, so log user in
        profile = oauth.get(settings.GREETINGS_PROFILE_URL).json()
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
