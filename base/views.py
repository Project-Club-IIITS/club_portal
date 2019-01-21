from time import sleep

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db import IntegrityError
from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView
from django.contrib.auth.models import User

from posts.models import Post, PostApprover
from .models import Notification

from .notifications import *

from .utils import run_in_background

from base.forms import ClubForm
from base.models import ClubModerator, Club, ClubMember, ClubMentor, ClubPresident, ClubSettings


@run_in_background
def send_new_post_notification(request, post):
    if post.notify_followers:
        receiver_users = None
        if post.is_public:
            receiver_users = [up.user for up in post.club.following_user_profiles.all()]
        else:
            receiver_users = [m.user for m in post.club.clubmember_set.all()]

        sendNotification(request.user,
                         post.club,
                         receiver_users,
                         "New Post",
                         "A New Post",
                         'new_post'
                         )

        sendEmailNotification(
            receivers=receiver_users,
            title="New Post",
            message="New Post Email",
            from_email=post.author.email,
            html_message=""
        )


class IndexView(TemplateView):
    template_name = "base/index.html"


class NotificationView(TemplateView):
    template_name = "base/notifications.html"


def club_home(request):
    return render(request, 'base/all_clubs.html')


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
def add_member(request, club_name_slug, username=None):
    if username is None:
        username = request.GET.get('username', None)
        if username is None:
            raise Http404("No username supplied")

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

    if members[0].user != club.clubpresident.user:
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


@login_required
def request_join(request, club_name_slug):
    club_name = club_name_slug.replace('-', ' ')
    club = get_object_or_404(Club, name=club_name)

    try:
        ClubMember.objects.create(club=club, user=request.user, is_approved=False)
    except IntegrityError:
        pass

    return redirect('posts:club_posts', club_name_slug)


@login_required
def add_moderator(request, club_name_slug, username=None):
    if username is None:
        username = request.GET.get('username', None)
        if username is None:
            raise Http404("No username supplied")

    club_name = club_name_slug.replace('-', ' ')
    club = get_object_or_404(Club, name=club_name)

    if (hasattr(club, 'clubpresident') and club.clubpresident.user != request.user) and (
            not ClubMentor.objects.filter(club=club, user=request.user).exists()):
        raise PermissionDenied("You do not have permission to perform this action")

    user = get_object_or_404(User, username=username)

    try:
        ClubModerator.objects.create(club=club, user=user)
    except IntegrityError:
        pass

    return redirect('base:moderator_list', club_name_slug)


@login_required
def remove_moderator(request, club_name_slug, username=None):
    if username is None:
        username = request.GET.get('username', None)
        if username is None:
            raise Http404("No username supplied")

    club_name = club_name_slug.replace('-', ' ')
    club = get_object_or_404(Club, name=club_name)

    if (hasattr(club, 'clubpresident') and club.clubpresident.user != request.user) and (
            not ClubMentor.objects.filter(club=club, user=request.user).exists()):
        raise PermissionDenied("You do not have permission to perform this action")

    user = get_object_or_404(User, username=username)

    mod = user.clubmoderator_set.filter(club=club)

    # try:
    if mod.exists():
        mod.delete()
    # except IntegrityError:
    #     pass

    return redirect('base:moderator_list', club_name_slug)


@login_required
def approve_post(request, club_name_slug, encrypted_id):
    club_name = club_name_slug.replace('-', ' ')
    club = get_object_or_404(Club, name=club_name)

    if not ClubModerator.objects.filter(club=club, user=request.user).exists():
        raise PermissionDenied()

    post = get_object_or_404(Post, club=club, encrypted_id=encrypted_id)

    try:

        post_approver = PostApprover.objects.create(user=request.user, post=post)
    except IntegrityError:
        pass

    post.is_approved = True

    post.save()

    send_new_post_notification(request, post)

    return redirect('base:pending_posts_list', club_name_slug)


@login_required
def reject_post(request, club_name_slug, encrypted_id):
    club_name = club_name_slug.replace('-', ' ')
    club = get_object_or_404(Club, name=club_name)

    if not ClubModerator.objects.filter(club=club, user=request.user).exists():
        raise PermissionDenied()

    post = get_object_or_404(Post, club=club, encrypted_id=encrypted_id)

    try:
        post.delete()
    except:
        pass

    return redirect('base:pending_posts_list', club_name_slug)


@login_required
def change_president(request, club_name_slug, username):
    club_name = club_name_slug.replace('-', ' ')
    club = get_object_or_404(Club, name=club_name)

    if (hasattr(club, 'clubpresident') and club.clubpresident.user != request.user) and (
            not ClubMentor.objects.filter(club=club, user=request.user).exists()):
        raise PermissionDenied("You do not have permission to perform this action")

    user = get_object_or_404(User, username=username)

    if hasattr(club, 'clubpresident'):
        club.clubpresident.user = user
        club.clubpresident.save()

    else:
        ClubPresident.objects.create(club=club, user=user)

    return redirect('base:club_settings', club_name_slug)


@login_required
def club_settings(request, club_name_slug):
    club_name = club_name_slug.replace('-', ' ')
    club = get_object_or_404(Club, name=club_name)
    if not ClubModerator.objects.filter(club=club, user=request.user).exists():
        raise PermissionDenied("You are not allowed to access this page")

    if request.method == "POST":
        club_form = ClubForm(request.POST, request.FILES, instance=club)

        if club_form.is_valid():
            club = club_form.save()
            if 'back_img' in request.FILES:
                club.back_img = request.FILES['back_img']
                club.save()
            return redirect('base:club_settings', club.slug)
    else:
        club_form = ClubForm(instance=club)

    return render(request, 'base/club/settings.html',
                  {"club": club, "club_name_slug": club_name_slug, "club_form": club_form})


@login_required
def club_groups(request, club_name_slug):
    club_name = club_name_slug.replace('-', ' ')
    club = get_object_or_404(Club, name=club_name)
    if not ClubModerator.objects.filter(club=club, user=request.user).exists():
        raise PermissionDenied("You are not allowed to access this page")

    return render(request, 'base/club/groups.html', {"club": club, "club_name_slug": club_name_slug, })


def sendNotificationToClub(request):
    pass


@login_required
def follow_club(request, club_name_slug):
    club_name = club_name_slug.replace('-', ' ')
    club = get_object_or_404(Club, name=club_name)

    request.user.userprofile.following_clubs.add(club)

    return redirect('posts:club_posts', club_name_slug)


@login_required
def unfollow_club(request, club_name_slug):
    club_name = club_name_slug.replace('-', ' ')
    club = get_object_or_404(Club, name=club_name)

    request.user.userprofile.following_clubs.remove(club)

    return redirect('posts:club_posts', club_name_slug)
