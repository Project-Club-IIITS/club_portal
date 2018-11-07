from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_no = models.IntegerField()
    batch = models.CharField(max_length=150)
    roll_no = models.IntegerField()
    profile_pic = models.ImageField()
    status = models.CharField(max_length=150)
    following_clubs = models.ManyToManyField(User)


class GoogleAuth(models.Model):
    google_id = models.URLField()
    time_stamp = models.DateTimeField(auto_now_add=True)


class EmailConfirmation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_confirmed = models.BooleanField(default=False)
