from django.urls import path
from . import views

app_name = "posts"

urlpatterns = [
    path('', views.posts, name="posts"),
    path('post_detail', views.post_detail, name="post_detail")
]