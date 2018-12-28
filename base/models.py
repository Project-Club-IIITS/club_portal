from django.core.exceptions import ValidationError
from django.db import models


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
