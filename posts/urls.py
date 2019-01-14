from django.urls import path
from django.contrib.auth.views import TemplateView
from . import views

app_name = "posts"

urlpatterns = [
    path('<slug:club_name_slug>/create-poll/', views.createPoll
         , name='create_poll'),
    path('<slug:club_name_slug>/submit-poll/', views.submitPoll, name='submit_poll'),
    path('', views.posts, name='posts'),
    path('events/', views.events, name="events"),
    path('polls/', views.polls, name="polls"),
    path('<slug:club_name_slug>/', views.club_posts, name="club_posts"),
    path('<slug:club_name_slug>/events/', views.club_events, name="club_events"),
    path('<slug:club_name_slug>/polls/', views.club_polls, name="club_polls"),
    path('<slug:club_name_slug>/<int:encrypted_id>', views.post_detail, name="post_detail"),
    path('<slug:club_name_slug>/add-post', views.add_post, name="post-add"),
    path('<slug:club_name_slug>/edit-post/<int:id>', views.edit_post, name="post-edit"),
    path('<slug:club_name_slug>/<int:encrypted_id>/issue-update', views.post_update, name="post-update"),

    path('<slug:club_name_slug>/<int:encrypted_id>/vote', views.cast_vote, name='cast-vote'),
    path('like_post/<int:id>/', views.likePost, name='like-post'),
]
