from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.validators import validators
from django.db.models import signals
from django.dispatch import receiver
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken


# Create your models here.


@receiver(signals.pre_save, sender=User)
def revoke_tokens(sender, instance, update_fields, **kwargs):
    if not instance._state.adding:
        existing_user = User.objects.get(pk=instance.pk)
        if instance.password != existing_user.password or instance.email != existing_user.email or instance.username != existing_user.username:
            # If any of these params have changed, blacklist the tokens

            outstanding_tokens = OutstandingToken.objects.filter(user__pk=instance.pk)
            # Not checking for expiry date as cron is supposed to flush the expired tokens\
            # using manage.py flushexpiredtokens

            for out_token in outstanding_tokens:
                if hasattr(out_token, 'blacklistedtoken'):
                    # Token already blacklisted. Skip
                    continue

                BlacklistedToken.objects.create(token=out_token)
