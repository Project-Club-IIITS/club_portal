from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class check_date(models.Model):
    date = models.DateField()
    work_title = models.CharField(max_length = 34)
    user=models.ForeignKey(User,default='',on_delete=models.CASCADE)

    def __str__(self):
        return str(self.date) + ',' + str( self.work_title)

