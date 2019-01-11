from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.models import User

class IndexView(TemplateView):
    template_name = "base/index.html"



def usersList(request):
    userList = User.objects.all()

    context = {
        'userlist': userList
    }

    return render(request, 'base/moderator/makeMods.html', context)
