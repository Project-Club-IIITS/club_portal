from .models import Notification
from django.core.mail import send_mail

EMAIL_NOTIFICATION_TYPES = {
    'message':(),
    'new_post':(),
    'post_approved':(),
    'post_update':(),
    'added_member':(),
    'added_moderator':(),
}


def sendNotification(sender, club, receivers, title, message, type="message"):
    N = Notification.objects.create(
        sender=sender, club=club, title=title, message=message)

    N.receivers.add(*receivers)

    # sendEmailNotification(**locals())
    # sendPushNotification(**locals())


def sendEmailNotification(receivers, title, message, from_email, html_message):
    send_mail(subject=title,
              message=message,
              from_email=from_email,
              recipient_list=tuple(receiver.email for receiver in receivers),
              html_message=html_message,
              )


def send_appropriate_html_email(from_email, receivers, type, **kwargs):
    pass

def sendPushNotification(sender, club, receivers, title, message):
    pass
