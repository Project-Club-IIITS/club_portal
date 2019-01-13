from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from .models import Notification
from django.core.mail import send_mail


class IndexView(TemplateView):
    template_name = "base/index.html"


def usersList(request):
    userList = User.objects.all()

    context = {
        'userlist': userList
    }

    return render(request, 'base/moderator/makeMods.html', context)


def sendNotification(sender, club, receiver, title, message):
    Notification.objects.create(
        sender=sender, club=club, receiver=receiver, title=title, message=message)
    sendEmailNotification(**locals())
    sendPushNotification(**locals())


def sendEmailNotification(sender, club, receiver, title, message):
    send_mail(
        title,
        message,
        sender.email,
        ["sidm1999@gmail.com", ],
    )


def sendPushNotification(sender, club, receiver, title, message):
    pass
