from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.validators import validators
from base.models import Club
import os


def phone_number_validator(phone_number):
    try:
        phone_number = str(phone_number)
    except ValueError:
        raise validators.ValidationError('Invalid Input')

    if phone_number.isdigit() is False:
        raise validators.ValidationError('Phone numbers can only contain numbers')

    if not(10 <= len(phone_number) <= 11):
        raise validators.ValidationError('Length of phone number must be either 10 or 11')


def get_profilepic_upload_url(instance, filename):
    return os.path.join('accounts', str(instance.user.username), 'profile_pictures', filename)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_no = models.CharField(verbose_name='Phone Number', max_length=11, blank=True,
                                validators=[phone_number_validator])
    batch = models.CharField(max_length=150)
    roll_no = models.IntegerField()
    profile_pic = models.ImageField(upload_to=get_profilepic_upload_url, blank=True, null=True)
    following_clubs = models.ManyToManyField(Club)


class GoogleAuth(models.Model):
    google_id = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)


class EmailConfirmation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_confirmed = models.BooleanField(default=False)
