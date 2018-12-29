from django.urls import path
from . import views

app_name = "posts"

urlpatterns = [
    path('<slug:club_name_slug>/', views.posts, name="posts"),
    path('<slug:club_name_slug>/<int:encrypted_id>', views.post_detail, name="post_detail")
]