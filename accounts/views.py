from django.shortcuts import render

from base.models import ClubPresident, ClubModerator
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test

def ifAdmin(user):
    try:
        user.clubpresident
        return True
    except:
        return False



# @user_passes_test(ifAdmin)
def listForPresident(request):

    try:
        print(request.user.clubpresident_set.all())
    except:
        print('Not Done')




    users = User.objects.exclude(moderators)


    print(moderators)
    print(users)

    context = {
        'mods': moderators,
        'users': users
    }

    return render(request, 'accounts/listForPresident.html', context)
