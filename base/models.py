from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User



# Create your models here.

def club_name_validator(name):
    if '-' in name:
        raise ValidationError('The name can not contain \'-\'')

class Club(models.Model):
    name = models.CharField(max_length=100, validators=[club_name_validator])
    date_formed = models.DateField(auto_now_add=True)
    email = models.EmailField()
    about = models.TextField(help_text="Say a few lines about your club")
    is_active = models.BooleanField(default=True)
    is_supported = models.BooleanField(default=True)
    num_users = models.IntegerField(default=0)

    def __str__(self):
        return self.name


    def slug(self):
        return self.name.replace(' ','-')


class ClubPresident(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    club = models.OneToOneField(Club, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.user.username

    class Meta:
        unique_together = ('user', 'club')


class ClubModerator(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user.username + ' moderator')

    class Meta:
        unique_together = ('user', 'club')


class ClubMember(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.user.username + '-' + self.club.name

    class Meta:
        unique_together = ('user', 'club')
    
