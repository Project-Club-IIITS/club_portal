from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Club(models.Model):
    name = models.CharField(max_length=100)
    date_formed = models.DateField(auto_now_add=True)
    email = models.EmailField()
    is_active = models.BooleanField(default=True)
    is_supported = models.BooleanField(default=True)
    num_users = models.IntegerField(default=0)


class ClubPresident(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    club = models.OneToOneField(Club, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'club')


class ClubModerator(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'club')


class ClubMember(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'club')
