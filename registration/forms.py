from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from registration.models import GoogleAuth


class SignupForm(forms.ModelForm):
    # email = forms.EmailField(max_length=200, help_text='Required')
    password1 = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name',)

    def clean(self):
        cleaned_data = super().clean()

        if cleaned_data['password1'] != cleaned_data['password2']:
            self.add_error('password2', "Passwords do not match")

        if User.objects.filter(email=cleaned_data['email']).exists():
            self.add_error("email", "This email already exisis. Choose another one")

        if cleaned_data['email'].split('@')[1] != 'iiits.in':
            self.add_error("email", "Currently we are allowing only iiits emails")


class FirebaseGoogleLoginForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    # Replace all textareas with charfields
    full_name = forms.CharField(required=False)
    auth_token = forms.CharField(required=False)
    refresh_token = forms.CharField(required=False)
    next_url = forms.CharField(required=False)

    class Meta:
        model = GoogleAuth
        fields = ('firebase_uid', 'auth_token', 'refresh_token', 'profile_pic_link')
