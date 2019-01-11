from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path('<slug:club_name>/list-for-president/', views.listForPresident, name='list_for_president'),
    path('<slug:club_name>/list-for-moderator/', views.listForModerator, name='list_for_moderator'),
    path('makeMember/', views.makeMember, name='make_member'),
    path('makeModerator/', views.makeModerator, name='make_moderator'),
]
