from django.urls import path
from . import views
from django.contrib.auth.views import TemplateView

app_name = "base"

urlpatterns = [
    path('', TemplateView.as_view(template_name="base/index.html"), name='index'),
    path('user-list/', views.usersList, name='user_list'),
    path('clubs/', views.club_home, name='club-description'),
    path('member_list/', views.member_list, name='member_list'),
    path('moderator_list/', views.moderator_list, name='moderator_list'),
    path('pending_posts_list/', views.pending_posts_list, name='pending_posts_list'),

]
