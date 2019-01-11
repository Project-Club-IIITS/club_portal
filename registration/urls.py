from django.urls import path

from . import views

app_name = "registration"

urlpatterns = [
    path('choose-club', views.choose_club, name="choose-club")
]
