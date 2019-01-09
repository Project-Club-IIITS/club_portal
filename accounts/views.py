from django.shortcuts import render

from base.models import ClubPresident, ClubModerator, Club

# @user_passes_test(ifAdmin)
def listForPresident(request, club_name):

    club = Club.objects.get(name = club_name)

    try:
        if (club.clubpresident.user == request.user):
            moderators = club.clubmoderator_set.filter(is_approved=False)
        else:
            moderators = []
    except:
        moderators = []

    print(moderators)

    context = {
        'mods': moderators,
    }

    return render(request, 'accounts/listForPresident.html', context)



def listForModerator(request, club_name):

    club = Club.objects.get(name = club_name)

    try:
        club.clubmoderator_set.get(user=request.user)
        users = club.clubmember_set.filter(is_approved=False)
    except:
        print('except mein aya')
        users = []

    print(users)

    context = {
        'users': users,
    }

    return render(request, 'accounts/listForModerator.html', context)
