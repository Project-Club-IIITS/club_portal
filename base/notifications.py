from .models import Notification
from django.core.mail import send_mail


def sendNotification(sender, club, receivers, title, message):
    for receiver in receivers:
        Notification.objects.create(
            sender=sender, club=club, receiver=receiver, title=title, message=message)
    del(receiver)
    sendEmailNotification(**locals())
    sendPushNotification(**locals())


def sendEmailNotification(sender, club, receivers, title, message):
    send_mail(
        title,
        message,
        'tempsidm1999@gmail.com',
        tuple(receiver.email for receiver in receivers)
    )


def sendPushNotification(sender, club, receivers, title, message):
    pass
