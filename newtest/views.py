from django.shortcuts import render, redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.forms.models import model_to_dict


from django.contrib.auth import authenticate,login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

from django.conf import settings
from .models import Token
from .forms import EmailTemplatesForm
import utils

from django.utils import timezone
import datetime
import logging
import requests_oauthlib


def home(request):
    if request.user.is_authenticated():
        oauth = utils.oauth_session(callback=request.build_absolute_uri(reverse('greetings:authorize')))
        #~ patient_data=oauth.get("http://localhost:9000/patient1").json()
        #~ patients=patient_data["results"]
        patients=utils.get_patients(request.user)
        #~ return redirect('practice:index', name=form.cleaned_data['drchrono_user'])
        username=request.user.get_username()#request.session['username']
        context={'username': username, 'patient_list': patients}
        return render(request, 'newtest/index.html', context)
    return render(request,'newtest/splash.html')

def register(request):
    oauth=utils.oauth_session(callback=request.build_absolute_uri(reverse('greetings:authorize')))
    # https://drchrono.com/o/authorize
    authorization_url, state = oauth.authorization_url("http://localhost:9000/o/authorize")
    request.session['oauth_state'] = state
    request.session.modified = True
    return redirect(authorization_url)

def logout(request):
    auth_logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('greetings:home')

def fribble(request):
    user=authenticate(remote_user='batshit')
    login(request, user)
    return redirect('greetings:home')

# handle OAuth2 callback
def authorize(request):
    # handle explicit error parameters in redirect
    if 'error' in request.GET:
        messages.error(request, 'OAuth authentication with Dr Chrono failed.')
        return redirect('greetings:home')

    authorization_response = request.build_absolute_uri()
    oauth = utils.oauth_session(callback=request.build_absolute_uri(reverse('greetings:authorize')))
    token={}
    try:
        token = oauth.fetch_token(
                'http://localhost:9000/o/token/',
                authorization_response=authorization_response,
                client_secret=settings.OAUTH_CLIENT_SECRET)
    except:
        messages.error(request, 'Could not retrieve OAuth token from Dr Chrono.')
    if token:
        token['expires']=timezone.now() + datetime.timedelta(seconds=token['expires_at'])
        # token is valid, so log user in
        profile=oauth.get('http://localhost:9000/profile').json()
        user=authenticate(remote_user=profile['username'])
        login(request, user)
        #~ # serialize token information to database for later use.
        try: # fetch and update token
            tkn=user.token
            tkn.update(token)
            tkn.save()
        except Token.DoesNotExist: # new user, create token
            tkn=Token.from_dict(user, token)
            tkn.save()
    return redirect('greetings:home')

@login_required(login_url='greetings:home')
def settings_view(request):
    templatedata=request.user.emailtemplates
    # save post and reload page
    if request.method == 'POST':
        form = EmailTemplatesForm(request.POST, initial=model_to_dict(templatedata), instance=templatedata)
        if form.is_valid():
            if form.has_changed():
                form.save()
                messages.success(request, 'Acccount settings updated.')
            return redirect('greetings:settings')
    else:
        form = EmailTemplatesForm(initial=model_to_dict(templatedata))

    return render(request, 'newtest/manage.html', {'email_templates': form})

@login_required(login_url='greetings:home')
def delete(request):
    return HttpResponse('delete!')

