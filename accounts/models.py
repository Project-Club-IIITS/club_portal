from django.contrib.auth.models import User
from django.db import models
from posts.models import Event


# Create your models here.
class Calendar(models.Model):
    # event = models.ForeignKey(to=Event, on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # Following fields required only if event is None

    title = models.CharField(max_length=200, null=True, blank=True)
    date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.user.username) + ',' + str(self.title)
