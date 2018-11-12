from django.urls import path

app_name = "registration"
from registration import views

urlpatterns = [
	path('login/', views.login,name='login'),
	path('signup/', views.signup,name='signup'),
]