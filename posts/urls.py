from django.urls import path
from . import views

app_name = "posts"

urlpatterns = [
    path('<slug:club_name_slug>/', views.posts, name="posts"),
    path('<slug:club_name_slug>/<int:encrypted_id>', views.post_detail, name="post_detail"),
    path('<slug:club_name_slug>/events/create',views.events_create, name="events_create"),
    path('<slug:club_name_slug>/events/update/<int:encrypted_id>',views.events_update, name="events_update"),
]