from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenObtainSerializer
from firebase_admin import auth
from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.six import text_type


# class UIDField(serializers.CharField):
#     def __init__(self, *args, **kwargs):
#         kwargs.setdefault('style', {})
#
#         kwargs['style']['input_type'] = 'uid'
#         kwargs['write_only'] = True
#
#         super(UIDField, self).__init__(*args, **kwargs)


class FirebaseTokenObtainSerializer(serializers.Serializer):
    email_field = User.EMAIL_FIELD

    def __init__(self, *args, **kwargs):
        super(FirebaseTokenObtainSerializer, self).__init__(*args, **kwargs)

        self.fields[self.email_field] = serializers.CharField()
        self.fields['uid'] = serializers.CharField()
        self.user = None

    def validate(self, attrs):
        email = attrs['email']
        uid = attrs['uid']

        try:
            firebase_user = auth.get_user(uid)
            if firebase_user.email != email:
                raise serializers.ValidationError(
                    _('Invalid Credentials'),
                )
            self.user = User.objects.get(email=email)
        except:
            raise serializers.ValidationError(
                _('No active account found with the given credentials'),
            )

        return {}


class FirebaseTokenObtainPairSerializer(FirebaseTokenObtainSerializer):
    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def validate(self, attrs):
        data = super(FirebaseTokenObtainPairSerializer, self).validate(attrs)

        refresh = self.get_token(self.user)

        data['refresh'] = text_type(refresh)
        data['access'] = text_type(refresh.access_token)

        return data
