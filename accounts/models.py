from django.contrib.auth.models import User
from django.db import models
from posts.models import Event


# Create your models here.
class Calendar(models.Model):
    date = models.DateField()
    work_title = models.CharField(max_length=34)
    user = models.ForeignKey(User, default='', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.date) + ',' + str(self.work_title)
