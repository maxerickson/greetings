from django.conf.urls import include,url

from . import views

app_name="greetings"

urlpatterns = [
    url(r'^authorize$', views.authorize, name='authorize'),
    url(r'^register$', views.register, name='register'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^settings$', views.settings_view, name='settings'),
    url(r'^settings/delete', views.delete, name='delete'),
    url(r'^', views.home, name='home'),
]
