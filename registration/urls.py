from django.urls import path, include
from django.conf.urls import url
from . import views
app_name = "registration"

urlpatterns = [
    url('^', include('django.contrib.auth.urls')),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
]