import os

from django.db import models
from django.contrib.auth.models import User
from django.db.models import signals
from django.dispatch import receiver

from base.models import Club
from ckeditor_uploader.fields import RichTextUploadingField
# Create your models here.
from posts.utils import encrypt_id


def cover_image_upload_path(instance, filename):
    return os.path.join('clubs', instance.club.name, 'posts', str(instance.id), 'cover', filename)


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)
    title = models.CharField(max_length=150)
    body = RichTextUploadingField()  # from ckeditor
    is_public = models.BooleanField(default=False)
    cover_image = models.ImageField(null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)

    last_updated = models.DateTimeField(auto_now=True)

    votes = models.IntegerField(default=0)

    encrypted_id = models.BigIntegerField(default=0, editable=False, db_index=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title[:20]


class PinnedPost(models.Model):
    post = models.OneToOneField(to=Post, on_delete=models.CASCADE)


class Image(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image = models.ImageField()


class Poll(models.Model):
    post = models.OneToOneField(Post, on_delete=models.CASCADE)


class Option(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    option = models.CharField(max_length=150)
    num_votes = models.IntegerField(default=0)


class Vote(models.Model):
    option = models.ForeignKey(Option, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time_stamp = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=264)
    time_stamp = models.DateTimeField(auto_now_add=True)


@receiver(signals.post_save, sender=Post)
def create_profile_and_oauth(sender, instance, created, **kwargs):
    if created:
        instance.encrypted_id = encrypt_id(instance.id)
        instance.save()
