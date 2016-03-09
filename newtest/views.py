from django.shortcuts import render, redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.core.urlresolvers import reverse

from django.contrib.auth import authenticate,login
from django.contrib.auth.models import User

from django.conf import settings
from .models import Token
import utils

from django.utils import timezone
import datetime
import logging
import requests_oauthlib


def home(request):
    if request.user.is_authenticated():
        oauth = utils.oauth_session(callback=request.build_absolute_uri(reverse('greetings:authorize')))
        patient_data=oauth.get("http://localhost:9000/patient1").json()
        patients=patient_data["results"]
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

def fribble(request):
    user=authenticate(remote_user='batshit')
    login(request, user)
    return redirect('greetings:home')

# handle OAuth2 callback
def authorize(request):
    authorization_response = request.build_absolute_uri()
    print request.session['oauth_state']
    oauth = utils.oauth_session(callback=request.build_absolute_uri(reverse('greetings:authorize')))
    token = oauth.fetch_token(
            'http://localhost:9000/o/token/',
            authorization_response=authorization_response,
            client_secret=settings.OAUTH_CLIENT_SECRET)
    token['expires']=timezone.now() + datetime.timedelta(seconds=token['expires_at'])
    # token is valid, so log user in
    profile=oauth.get('http://localhost:9000/profile').json()
    user=authenticate(remote_user=profile['username'])
    login(request, user)
    # serialize token information to database for use when generating emails.
    #~ try: # fetch and update token
        #~ tkn=user.token
        #~ tkn.access_token=token['access_token']
        #~ tkn.refresh_token=token['refresh_token']
        #~ tkn.expires=token['expires']
        #~ tkn.save()
    #~ except Token.DoesNotExist: # new user, create token
        #~ tkn=Token(user=user, access_token=token['access_token'], refresh_token=token['refresh_token'], expires=token['expires'])
        #~ tkn.save()

    return redirect('greetings:home')

