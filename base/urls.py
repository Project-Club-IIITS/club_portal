from django.urls import path
from . import views
from django.contrib.auth.views import TemplateView

app_name = "base"

urlpatterns = [
    path('', TemplateView.as_view(template_name="base/index.html"), name='index'),
    path('clubs/', views.club_home, name='all_clubs'),
    path('clubs/<slug:club_name_slug>/members/', views.member_list, name='member_list'),
    path('clubs/<slug:club_name_slug>/members/add/<str:username>/', views.add_member, name='add_member'),
    path('clubs/<slug:club_name_slug>/members/remove/<str:username>/', views.remove_member, name='remove_member'),
    path('clubs/<slug:club_name_slug>/members/approve/<str:username>/', views.approve_member, name='approve_member'),
    path('clubs/<slug:club_name_slug>/moderators/', views.moderator_list, name='moderator_list'),
    path('clubs/<slug:club_name_slug>/pending_posts/', views.pending_posts_list, name='pending_posts_list'),

]
