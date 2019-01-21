from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, HttpResponse

from accounts.forms import PasswordResetForm
from base.models import ClubPresident, ClubModerator, Club, ClubMember
from django.contrib.auth.models import User

# Calendar imports

from django.shortcuts import render



def listForPresident(request, club_name):
    club = Club.objects.get(name=club_name)

    try:
        if club.clubpresident.user == request.user:
            moderators = club.clubmoderator_set.filter(is_approved=False)
        else:
            moderators = []
    except:
        moderators = []


    context = {
        'mods': moderators,
        'club_name': club_name
    }

    return render(request, 'accounts/listForPresident.html', context)


def listForModerator(request, club_name):
    club = Club.objects.get(name=club_name)
    try:
        club.clubmoderator_set.get(user=request.user)
        users = club.clubmember_set.filter(is_approved=False)
    except:
        users = []

    context = {
        'users': users,
        'club_name': club_name
    }

    return render(request, 'accounts/listForModerator.html', context)


def makeModerator(request):
    if request.method == 'POST':
        username = request.POST.get('username', None)
        club = request.POST.get('club_name', None)

        user = User.objects.get(username=username)
        club = Club.objects.get(name=club)

        new_member = ClubModerator.objects.get(user=user, club=club)
        new_member.is_approved = True
        new_member.save()

        data = {

        }

        return JsonResponse(data)


def makeMember(request):
    if request.method == 'POST':
        username = request.POST.get('username', None)
        club = request.POST.get('club_name', None)

        user = User.objects.get(username=username)
        club = Club.objects.get(name=club)

        new_member = ClubMember.objects.get(user=user, club=club)
        new_member.is_approved = True
        new_member.save()

        data = {

        }

        return JsonResponse(data)


def makeModerator(request):
    if request.method == 'POST':
        username = request.POST.get('username', None)
        club = request.POST.get('club_name', None)

        user = User.objects.get(username=username)
        club = Club.objects.get(name=club)

        new_member = ClubModerator.objects.get(user=user, club=club)
        new_member.is_approved = True
        new_member.save()

        data = {

        }

        return JsonResponse(data)


@login_required
def change_password(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)

        if password_reset_form.is_valid():
            if request.user.has_usable_password():
                if request.user.check_password(password_reset_form.cleaned_data['old_password']):
                    request.user.set_password(password_reset_form.cleaned_data['new_password'])
                    request.user.save()
                    login(request, request.user)
                    return redirect('accounts:profile')
                else:
                    password_reset_form.add_error('old_password', 'Incorrect Old Password')

            else:
                request.user.set_password(password_reset_form.cleaned_data['new_password'])
                request.user.save()
                login(request, request.user)
                return redirect('accounts:profile')
    else:
        password_reset_form = PasswordResetForm()

    return render(request, 'accounts/change_password.html', {'form': password_reset_form})


@login_required
def profile(request):
    context = {
        'posts': request.user.post_set.all(),
        'member_club': request.user.clubmember_set.all()
    }

    return render(request, 'accounts/profile.html', context)


# from first_app.forms import calendar_data
# Create your views here.
next_m = 0
next_y = 0
back_m = 0
back_y = 0


