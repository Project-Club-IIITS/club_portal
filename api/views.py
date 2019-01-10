from django.http import JsonResponse
from django.urls import reverse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.sites.shortcuts import get_current_site
import requests
from rest_framework_simplejwt.views import TokenViewBase
from . import serializers


class HelloView(APIView):
    # permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Hello, World!'}
        # return requests

        domain = get_current_site(request).domain
        url = reverse('api:token_obtain_pair')
        return JsonResponse(requests.post(f'http://{domain}{url}', data={'username': 'a', 'password': 'b'}).json())


class FirebaseTokenObtainPairView(TokenViewBase):
    """
    Takes a set of user credentials and returns an access and refresh JSON web
    token pair to prove the authentication of those credentials.
    """
    serializer_class = serializers.FirebaseTokenObtainPairSerializer


firebase_token_obtain_pair = FirebaseTokenObtainPairView.as_view()
