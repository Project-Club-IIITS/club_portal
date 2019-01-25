from django.urls import path
from . import views
from django.contrib.auth.views import TemplateView

app_name = "base"

urlpatterns = [

    path('', TemplateView.as_view(template_name="base/index.html"), name='index'),
    path('clubs/', views.club_home, name='all_clubs'),
    path('clubs/<slug:club_name_slug>/request-join/', views.request_join, name='club_request_join'),
    path('clubs/<slug:club_name_slug>/follow/', views.follow_club, name='club_follow'),
    path('clubs/<slug:club_name_slug>/unfollow/', views.unfollow_club, name='club_unfollow'),

    path('clubs/<slug:club_name_slug>/admin/settings/', views.club_settings, name='club_settings'),
    path('clubs/<slug:club_name_slug>/admin/members/', views.member_list, name='member_list'),
    path('clubs/<slug:club_name_slug>/admin/moderators/', views.moderator_list, name='moderator_list'),
    path('clubs/<slug:club_name_slug>/admin/pending_posts/', views.pending_posts_list, name='pending_posts_list'),
    path('clubs/<slug:club_name_slug>/admin/groups/', views.club_groups, name='club_groups'),

    path('clubs/<slug:club_name_slug>/members/add/', views.add_member, name='add_member_name_as_param'),
    path('clubs/<slug:club_name_slug>/members/add/<str:username>/', views.add_member, name='add_member'),
    path('clubs/<slug:club_name_slug>/members/remove/<str:username>/', views.remove_member, name='remove_member'),
    path('clubs/<slug:club_name_slug>/members/approve/<str:username>/', views.approve_member, name='approve_member'),

    path('clubs/<slug:club_name_slug>/moderators/add/', views.add_moderator, name='add_moderator_name_as_param'),
    path('clubs/<slug:club_name_slug>/moderators/add/<str:username>/', views.add_moderator, name='add_moderator'),
    path('clubs/<slug:club_name_slug>/moderators/remove/', views.remove_moderator,
         name='remove_moderator_name_as_param'),
    path('clubs/<slug:club_name_slug>/moderators/remove/<str:username>/', views.remove_moderator,
         name='remove_moderator'),

    path('clubs/<slug:club_name_slug>/posts/approve/<int:encrypted_id>/', views.approve_post, name="approve_post"),
    path('clubs/<slug:club_name_slug>/posts/reject/<int:encrypted_id>/', views.reject_post, name="reject_post"),

    path('notifications', views.NotificationView.as_view(), name='notifications'),

    path('post_email_temp', views.post_email_temp)

]
