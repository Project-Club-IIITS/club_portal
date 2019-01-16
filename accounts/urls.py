from django.urls import path
from . import views
from django.views.generic import TemplateView

app_name = "accounts"

urlpatterns = [
    path('change-password', views.change_password, name='password-change'),
    path('<slug:club_name>/list-for-president/', views.listForPresident, name='list_for_president'),
    path('<slug:club_name>/list-for-moderator/', views.listForModerator, name='list_for_moderator'),
    path('makeMember/', views.makeMember, name='make_member'),
    path('makeModerator/', views.makeModerator, name='make_moderator'),
    path('profile/', views.profile, name='profile')
]
