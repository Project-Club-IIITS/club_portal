from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from api import views

app_name = 'api'

urlpatterns = [
    # Your URLs...
    path('token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('test', views.HelloView.as_view(), name="hello"),
]