from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from django.contrib.auth.models import User

from base.models import ClubModerator, Club, ClubMember


class IndexView(TemplateView):
    template_name = "base/index.html"


def club_home(request):
    return render(request, 'base/club/index.html')


@login_required
def member_list(request, club_name_slug):
    club_name = club_name_slug.replace('-', ' ')
    club = get_object_or_404(Club, name=club_name)

    if not ClubModerator.objects.filter(club=club, user=request.user).exists():
        raise PermissionDenied("You are not allowed to access this page")

    members = ClubMember.objects.filter(club=club, is_approved=True)
    pending_members = ClubMember.objects.filter(club=club, is_approved=False)
    return render(request, 'base/club/member.html', {"club": club, "members": members, "club_name_slug": club_name_slug,
                                                     "pending_members": pending_members})


@login_required
def moderator_list(request, club_name_slug):
    club_name = club_name_slug.replace('-', ' ')
    club = get_object_or_404(Club, name=club_name)

    if club.clubpresident.user != request.user:
        raise PermissionDenied("You are not allowed to access this page")

    moderators = ClubModerator.objects.filter(club=club)
    return render(request, 'base/club/moderator.html',
                  {"club": club, "club_name_slug": club_name_slug, "moderators": moderators})


@login_required
def pending_posts_list(request, club_name_slug):
    club_name = club_name_slug.replace('-', ' ')
    club = get_object_or_404(Club, name=club_name)

    if not ClubModerator.objects.filter(club=club, user=request.user).exists():
        raise PermissionDenied("You are not allowed to access this page")

    pending_posts = club.post_set.filter(is_approved=False)

    return render(request, 'base/club/pendingPosts.html',
                  {"club": club, "club_name_slug": club_name_slug, "pending_posts": pending_posts})
