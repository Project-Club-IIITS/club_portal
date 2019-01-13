from .models import Notification
from django.core.mail import send_mail


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
        [receiver.email, ],
    )


def sendPushNotification(sender, club, receiver, title, message):
    pass
