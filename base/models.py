from django.core.exceptions import ValidationError
from django.db import models, IntegrityError, transaction
from django.contrib.auth.models import User

# Create your models here.
from django.db.models import signals, ProtectedError
from django.dispatch import receiver


def club_name_validator(name):
    if '-' in name:
        raise ValidationError('The name can not contain \'-\'')


class Club(models.Model):
    name = models.CharField(max_length=100, validators=[club_name_validator], db_index=True)
    date_formed = models.DateField(auto_now_add=True)
    email = models.EmailField()
    about = models.TextField(help_text="Say a few lines about your club")
    is_active = models.BooleanField(default=True)
    is_supported = models.BooleanField(default=True)
    num_users = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def slug(self):
        return self.name.replace(' ', '-')


class ClubPresident(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    # We can't allow user to be deleted unless new president is set
    club = models.OneToOneField(Club, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

    class Meta:
        unique_together = ('user', 'club')


class ClubModerator(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user.username + ' moderator')

    class Meta:
        unique_together = ('user', 'club')


class ClubMember(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username + '-' + self.club.name

    class Meta:
        unique_together = ('user', 'club')


@receiver(signals.post_save, sender=ClubModerator)
def moderator_add_member(sender, instance, created, **kwargs):
    # If a user is made a moderator, also make him a member of the club
        try:
            with transaction.atomic():  # We need to make atomic as code may throw integrity error
                ClubMember.objects.create(user=instance.user, club=instance.club, is_approved=True)
        except IntegrityError:
            # User is already a member. Do Nothing
            pass


@receiver(signals.post_save, sender=ClubPresident)
def president_add_moderator_member(sender, instance, created, **kwargs):
    # If a user is made a president, also make him a member and moderator of the club
        try:
            with transaction.atomic():  # We need to make atomic as code may throw integrity error
                ClubModerator.objects.create(user=instance.user, club=instance.club)
            # Just making moderator is enough, as while making moderator, the above signal will be called, which will make him a member
        except IntegrityError:
            # User is already a moderator. Do Nothing
            pass


@receiver(signals.pre_delete, sender=ClubModerator)
def moderator_delete_protect_president(sender, instance, **kwargs):
    # If a moderator is deleted, and if user is also president, prevent delete of moderator
    if instance.club.clubpresident.user == instance.user:
        raise ProtectedError("Can not delete moderator who is also president", instance)


@receiver(signals.pre_delete, sender=ClubMember)
def member_delete_moderator(sender, instance, **kwargs):
    # If a member is deleted, also delete moderator

    mod_instance = ClubModerator.objects.filter(user=instance.user, club=instance.club)
    if mod_instance.exists():
        mod_instance.delete()
