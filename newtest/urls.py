from django.conf.urls import include,url

from . import views

app_name="greetings"

urlpatterns = [
    url(r'^authorize$', views.authorize, name='authorize'),
    url(r'^register$', views.register, name='register'),
    url(r'^fribble$', views.fribble, name='fribble'),
    url(r'^', views.home, name='home'),
]
