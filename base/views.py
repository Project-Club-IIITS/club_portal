from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
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


@login_required
def add_member(request, club_name_slug, username):
    club_name = club_name_slug.replace('-', ' ')
    club = get_object_or_404(Club, name=club_name)

    if not ClubModerator.objects.filter(club=club, user=request.user).exists():
        raise PermissionDenied("You are not allowed to access this page")

    users = User.objects.filter(username=username)
    if not users.exists():
        return HttpResponse("This user does not exist")

    user = users[0]
    try:
        ClubMember.objects.create(club=club, user=user, is_approved=True)
    except IntegrityError:
        pass

    return redirect('base:member_list', club_name_slug)


@login_required
def remove_member(request, club_name_slug, username):
    club_name = club_name_slug.replace('-', ' ')
    club = get_object_or_404(Club, name=club_name)

    if not ClubModerator.objects.filter(club=club, user=request.user).exists():
        raise PermissionDenied("You are not allowed to access this page")

    members = ClubMember.objects.filter(club=club, user__username=username)
    if not members.exists():
        return HttpResponse("This user does not exist")

    try:
        members[0].delete()
    except:
        return HttpResponse("Some error occured. Try again later")

    return redirect('base:member_list', club_name_slug)


@login_required
def approve_member(request, club_name_slug, username):
    club_name = club_name_slug.replace('-', ' ')
    club = get_object_or_404(Club, name=club_name)

    if not ClubModerator.objects.filter(club=club, user=request.user).exists():
        raise PermissionDenied("You are not allowed to access this page")

    members = ClubMember.objects.filter(club=club, user__username=username)
    if not members.exists():
        return HttpResponse("This user does not exist")

    member = members[0]
    try:
        member.is_approved = True
        member.save()
    except:
        return HttpResponse("Some error occured. Try again later")

    return redirect('base:member_list', club_name_slug)


def request_join(request, club_name_slug):
    club_name = club_name_slug.replace('-', ' ')
    club = get_object_or_404(Club, name=club_name)

    if not request.user.is_authenticated:
        raise PermissionDenied()

    try:
        ClubMember.objects.create(club=club, user=request.user, is_approved=False)
    except IntegrityError:
        pass

    return redirect('posts:club_posts', club_name_slug)
