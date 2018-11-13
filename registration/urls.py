from django.urls import path, include
from django.conf.urls import url
app_name = "registration"

urlpatterns = [
    url('^', include('django.contrib.auth.urls')),
]