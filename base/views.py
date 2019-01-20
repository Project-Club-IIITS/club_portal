from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from .models import Notification

from .notifications import *


class IndexView(TemplateView):
    template_name = "base/index.html"


class NotificationView(TemplateView):
    template_name = "base/notifications.html"


def usersList(request):
    userList = User.objects.all()

    context = {
        'userlist': userList
    }

    return render(request, 'base/moderator/makeMods.html', context)


def sendNotificationToClub(request):
    pass
