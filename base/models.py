from django.db import models


# Create your models here.

class Club(models.Model):
    name = models.CharField(max_length=100)
    date_formed = models.DateField(auto_now_add=True)
    email = models.EmailField()
    is_active = models.BooleanField(default=True)
    is_supported = models.BooleanField(default=True)
    num_users = models.IntegerField(default=0)


