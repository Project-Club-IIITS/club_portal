from django.db import models
from django.contrib.auth.models import User
from base.models import Club


# Create your models here.

class Post(models.Model):
    post_creator = models.ForeignKey(User, on_delete=models.CASCADE)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    is_approved = models.BooleanField()
    description = models.TextField(max_length=150)
    video = models.URLField()


class Image(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image_url = models.URLField()
    is_public = models.BooleanField(default=False)


class Poll(models.Model):
    post = models.OneToOneField(Post, on_delete=models.CASCADE)


class Option(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    options = models.CharField(max_length=150)
    num_votes = models.IntegerField(default=0)


class Vote(models.Model):
    option = models.ForeignKey(Option, on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    time_stamp = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=264)
    time_stamp = models.DateTimeField(auto_now_add=True)
