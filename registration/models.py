from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.validators import validators
from django.db.models import signals
from django.dispatch import receiver

from base.models import Club
import os


def phone_number_validator(phone_number):
    try:
        phone_number = str(phone_number)
    except ValueError:
        raise validators.ValidationError('Invalid Input')

    if phone_number.isdigit() is False:
        raise validators.ValidationError('Phone numbers can only contain numbers')

    if not (10 <= len(phone_number) <= 11):
        raise validators.ValidationError('Length of phone number must be either 10 or 11')


def get_profilepic_upload_url(instance, filename):
    return os.path.join('accounts', str(instance.user.username), 'profile_pictures', filename)


class UserProfile(models.Model):
    BATCH_CHOICES = (
        ('UG1', 'UG1'),
        ('UG2', 'UG2'),
        ('UG3', 'UG3'),
        ('UG4', 'UG4'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_no = models.CharField(verbose_name='Phone Number', max_length=11, blank=True,
                                validators=[phone_number_validator])
    batch = models.CharField(max_length=3, choices=BATCH_CHOICES)
    roll_no = models.CharField(max_length=100)
    profile_pic = models.ImageField(upload_to=get_profilepic_upload_url, blank=True, null=True)
    following_clubs = models.ManyToManyField(Club)


class GoogleAuth(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    firebase_uid = models.CharField(max_length=150, default=' ')
    auth_token = models.TextField(null=True, blank=True)
    refresh_token = models.TextField(null=True, blank=True)
    profile_pic_link = models.URLField(null=True, blank=True)



class EmailConfirmation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


@receiver(signals.post_save, sender=User)
def set_email_confirmed_false(sender, instance, created, **kwargs):
    if created:
        EmailConfirmation.objects.create(user=instance)

        # Users passsing via oauth don't need to confirm email
        if instance.has_usable_password() is False:
            instance.emailconfirmation.email_confirmed = True

        # Superusers don't need to confirm emails
        elif instance.is_superuser:
            instance.emailconfirmation.email_confirmed = True

        instance.emailconfirmation.save()


@receiver(signals.post_save, sender=User)
def create_profile_and_oauth(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        GoogleAuth.objects.create(user=instance)
