from django.http import JsonResponse
from django.shortcuts import render

from base.models import ClubPresident, ClubModerator, Club, ClubMember
from django.contrib.auth.models import User


def listForPresident(request, club_name):

    club = Club.objects.get(name=club_name)

    try:
        if club.clubpresident.user == request.user:
            moderators = club.clubmoderator_set.filter(is_approved=False)
        else:
            moderators = []
    except:
        moderators = []

    print(moderators)

    context = {
        'mods': moderators,
        'club_name': club_name
    }

    return render(request, 'accounts/listForPresident.html', context)



def listForModerator(request, club_name):
    club = Club.objects.get(name = club_name)
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

