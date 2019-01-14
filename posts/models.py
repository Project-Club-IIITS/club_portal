import os

from django.core.exceptions import ValidationError
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

    title = models.CharField(max_length=150)
    body = RichTextUploadingField(blank=True)  # from ckeditor
    is_public = models.BooleanField(default=False)
    cover_image = models.ImageField(null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)

    last_updated = models.DateTimeField(auto_now=True)

    votes = models.IntegerField(default=0)

    encrypted_id = models.BigIntegerField(default=0, editable=False, db_index=True)

    subscribed_users = models.ManyToManyField(User, blank=True, related_name="subscribers")

    is_approved = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True,
                                       help_text="Uncheck this if you just want to save as draft and edit later before publishing")

    liked_users = models.ManyToManyField(User, related_name='liked_users', blank=True)

    class Meta:
        ordering = ['-last_updated']

    def __str__(self):
        return self.title[:20]


class PostUpdate(models.Model):
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['post', '-last_updated']


class PinnedPost(models.Model):
    post = models.OneToOneField(to=Post, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-post__last_updated']

    def clean(self):
        if self.post.is_approved is False:
            raise ValidationError("A post that has not been approved can not be pinned")


class Image(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image = models.ImageField()


class Poll(models.Model):
    post = models.OneToOneField(Post, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True, help_text="Make it False when you wish to stop collecting votes")

    track_votes = models.BooleanField(default=True, help_text="If checked, it will be tracked, which user has voted for\
                                        which option. If unchecked, voting will be anonymous. (In both cases, each user \
                                        can vote only once)"
                                      )

    @property
    def total_votes(self):
        count = 0
        for option in self.option_set.all():
            count += option.num_votes

        return count


class Option(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    option_text = models.CharField(max_length=150)
    num_votes = models.IntegerField(default=0)

    def __str__(self):
        return self.poll.post.title[:10] + "... : " + self.option_text + ":" + str(self.num_votes)

class Vote(models.Model):
    poll = models.ForeignKey(to=Poll, on_delete=models.CASCADE)
    option = models.ForeignKey(Option, null=True, blank=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time_stamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'poll']  # One user can thus vote for only 1 option

    def __str__(self):
        return self.user.username + "-" + self.poll.post.title[:10] + "..."

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
