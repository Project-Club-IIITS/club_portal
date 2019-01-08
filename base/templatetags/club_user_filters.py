from django import template
from django.contrib.auth.models import User

from base.models import Club

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

    return club.clubmember_set.filter(user=user).exists()


@register.filter
def is_user_president(user, club):
    """
    Checks whether incoming user is a moderator for the club
    """
    if not (isinstance(user, User) and isinstance(club, Club)):
        raise ValueError("User must be an instance of User model and club must be an instance of Club model")

    return club.clubpresident.user == user

