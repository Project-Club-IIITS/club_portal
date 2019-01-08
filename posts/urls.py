from django.urls import path
from . import views

app_name = "posts"

urlpatterns = [
    path('<slug:club_name_slug>/', views.posts, name="posts"),
    path('<slug:club_name_slug>/<int:encrypted_id>', views.post_detail, name="post_detail"),
    path('<slug:club_name_slug>/add-post', views.add_post, name="post-add"),
    path('<slug:club_name_slug>/edit-post/<int:id>', views.edit_post, name="post-edit"),
]