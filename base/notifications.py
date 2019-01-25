from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.urls import reverse

from .models import Notification
from django.core.mail import send_mail

EMAIL_NOTIFICATION_TYPES = {
    'message': (),
    'new_post': (),
    'post_approved': (),
    'post_update': (),
    'added_member': (),
    'added_moderator': (),
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


def sendNewPostEmailNotification(request, receivers, post):
    receiver_emails = [u.email for u in receivers]

    subject = f'{post.club} has posted a new announcement'
    from_email_club_name = post.club.name.replace(' ', '_').lower()
    from_email = f'{from_email_club_name}@no_reply.clubs.iiits.in'

    current_site = get_current_site(request)

    html_message = render_to_string('base/emails/new_post.html', {"post": post, "domain": current_site.domain})

    non_html_message = """"
            A new announcement has been posted. . Clink the link to view it. """ + reverse('posts:post_detail',
                                                                                           args= [post.club.name.replace(' ','-'),
                                                                                           post.encrypted_id
                                                                                                  ]
                                                                                           )
    send_mail(subject=subject,
              message=non_html_message,
              from_email=from_email,
              recipient_list=receiver_emails,
              html_message=html_message
              )


def sendPostApprovedEmailNotification(request, post):
    subject = f'Your post has been approved'

    receiver_emails = [post.author.email]
    from_email_club_name = post.club.name.replace(' ', '_').lower()
    from_email = f'{from_email_club_name}@no_reply.clubs.iiits.in'

    current_site = get_current_site(request)

    html_message = render_to_string('base/emails/post_approved.html', {"post": post, "domain": current_site.domain})
    non_html_message = "Your post has been approved"

    send_mail(subject=subject,
              message=non_html_message,
              from_email=from_email,
              recipient_list=receiver_emails,
              html_message=html_message
              )


def sendPostUpdateEmailNotification(request, receivers, post_update):
    receiver_emails = [u.email for u in receivers]

    subject = f'{post_update.post.title} has a new update'
    from_email_club_name = post_update.post.club.name.replace(' ', '_').lower()
    from_email = f'{from_email_club_name}@no_reply.clubs.iiits.in'

    current_site = get_current_site(request)

    html_message = render_to_string('base/emails/post_update.html',
                                    {"post_update": post_update, "post": post_update.post,
                                     "domain": current_site.domain})

    non_html_message = """"
                A new update has been posted for this post.  Click to view """ + reverse('posts:post_detail',
                                                                                         args=[
                                                                                         post_update.post.club.name.replace(
                                                                                             ' ',
                                                                                             '-'),
                                                                                         post_update.post.encrypted_id
                                                                                                ]
                                                                                         )
    send_mail(subject=subject,
              message=non_html_message,
              from_email=from_email,
              recipient_list=receiver_emails,
              html_message=html_message
              )


def sendWelcomeEmail(request, user):
    receiver_emails = [user.email]

    subject = f'Welcome to IIITS Clubs Portal'
    from_email = f'support@no_reply.clubs.iiits.in'

    current_site = get_current_site(request)
    admin = User.objects.get(username='admin')
    html_message = render_to_string('base/emails/welcome.html',
                                    {"domain": current_site.domain, "admin": admin})

    non_html_message = """"
                    Welcome to IIITS Clubs Portal. Your account has been successfully activated """

    send_mail(subject=subject,
              message=non_html_message,
              from_email=from_email,
              recipient_list=receiver_emails,
              html_message=html_message
              )

    print("email sent")
def send_appropriate_html_email(from_email, receivers, type, **kwargs):
    pass


def sendPushNotification(sender, club, receivers, title, message):
    pass
