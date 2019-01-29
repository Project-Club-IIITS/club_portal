from django import template
from django.contrib.auth.models import User

from base.models import Club
from posts.models import Poll, Vote

register = template.Library()


@register.filter
def is_user_moderator(user, club):
    """
    Checks whether incoming user is a moderator for the club
    """
    if not (isinstance(user, User) and isinstance(club, Club)):
        raise ValueError("User must be an instance of User model and club must be an instance of Club model")

    return club.clubmoderator_set.filter(user=user).exists()


@register.filter
def is_user_member(user, club):
    """
    Checks whether incoming user is a moderator for the club
    """
    if not (isinstance(user, User) and isinstance(club, Club)):
        raise ValueError("User must be an instance of User model and club must be an instance of Club model")

    return club.clubmember_set.filter(user=user, is_approved=True).exists()


@register.filter
def is_user_president(user, club):
    """
    Checks whether incoming user is a moderator for the club
    """
    if not (isinstance(user, User) and isinstance(club, Club)):
        raise ValueError("User must be an instance of User model and club must be an instance of Club model")

    return club.clubpresident.user == user


@register.filter
def is_user_mentor(user, club):
    """
    Checks whether user is mentor for the club
    """
    if not (isinstance(user, User) and isinstance(club, Club)):
        raise ValueError("User must be an instance of User model and club must be an instance of Club model")

    return club.clubmentor_set.filter(user=user).exists()


@register.filter
def has_user_casted_vote(poll, user):
    """
    Checks whether this user has already voted for this poll
    """
    if not (isinstance(poll, Poll) and isinstance(user, User)):
        raise ValueError("User must be an instance of User model and poll must be an instance of Poll model")

    return Vote.objects.filter(poll=poll, user=user).exists()

@register.filter
def is_user_member_not_approved(user, club):
    """
    Checks whether incoming user is a moderator for the club
    """
    if not (isinstance(user, User) and isinstance(club, Club)):
        raise ValueError("User must be an instance of User model and club must be an instance of Club model")

    return club.clubmember_set.filter(user=user).exists()
