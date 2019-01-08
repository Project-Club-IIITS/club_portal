from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path('list-for-president/', views.listForPresident, name='list_for_president'),
]
