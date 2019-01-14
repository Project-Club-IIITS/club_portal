from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from registration.models import GoogleAuth


class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name')


class FirebaseGoogleLoginForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    # Replace all textareas with charfields
    full_name = forms.CharField(required=False)
    auth_token = forms.CharField(required=False)
    refresh_token = forms.CharField(required=False)

    class Meta:
        model = GoogleAuth
        fields = ('firebase_uid', 'auth_token', 'refresh_token', 'profile_pic_link')
