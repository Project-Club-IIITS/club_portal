from time import sleep

from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.urls import resolve

from base.notifications import sendWelcomeEmail
from base.utils import run_in_background
from posts.models import Post
from .forms import SignupForm, FirebaseGoogleLoginForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf.global_settings import EMAIL_HOST_USER as sender
from .models import EmailConfirmation

from firebase_admin import auth


@run_in_background
def send_welcome_email(request, user):
    sendWelcomeEmail(request, user)


def signup(request):
    fireform = FirebaseGoogleLoginForm()
    if request.method == 'POST':

        form = SignupForm(request.POST)

        if form.is_valid():
            user = form.save()
            user_email = EmailConfirmation.objects.get(user=user)
            user_email.is_confirmed = False
            user_email.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your Account.'
            message = render_to_string('registration/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            send_mail(mail_subject, message, sender, [to_email])
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = SignupForm()
    return render(request, 'registration/signup.html', {'form': form, 'fireform': fireform})


# Create your views here.

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.emailconfirmation.is_confirmed = True
        user.save()
        login(request, user)
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')


def choose_club(request):
    return render(request, 'registration/choose-club.html')


def google_signin(request):
    if request.method == "POST":
        google_form = FirebaseGoogleLoginForm(request.POST)
        if google_form.is_valid():
            # print(google_form.cleaned_data)
            users = User.objects.filter(email=google_form.cleaned_data['email'])
            if len(users) > 0 and google_form.cleaned_data['firebase_uid'] == users[0].googleauth.firebase_uid:
                # User already validated. Directly login
                login(request, users[0])
                try:
                    next_match = resolve(google_form.cleaned_data['next_url'])
                    return redirect(google_form.cleaned_data['next_url'])

                except:
                    return redirect('base:index')

            # User not validated or uid has changed
            try:
                firebase_user = auth.get_user(google_form.cleaned_data['firebase_uid'])
                if firebase_user.email != google_form.cleaned_data['email']:
                    raise ValidationError(" Email id does not match!")
            except:
                return HttpResponse("The Data we received could not be verified by Google. Please try to login using \
                email id and password."
                                    )

            if len(users) == 0:
                # Signup
                if google_form.cleaned_data['email'].split('@')[1] != "iiits.in":
                    return HttpResponse(
                        "Currenty we are allowing only iiits users to sign in. Please sign in with a iiits account ")
                new_user = User.objects.create(email=google_form.cleaned_data['email'],
                                               username=google_form.cleaned_data['email'].split('@')[0],
                                               )

                names = google_form.cleaned_data['full_name']
                names = names.split(' ')
                new_user.first_name = names[0]
                if len(names) > 1:
                    new_user.last_name = " ".join(names[1:])

                new_user.save()

                send_welcome_email(request, new_user)

            else:
                # Login
                new_user = users[0]

            # Attach form fields to model
            guser = new_user.googleauth
            guser.firebase_uid = google_form.cleaned_data['firebase_uid']
            guser.auth_token = google_form.cleaned_data['auth_token']
            guser.refresh_token = google_form.cleaned_data['refresh_token']
            guser.profile_pic_link = google_form.cleaned_data['profile_pic_link']
            guser.save()

            login(request, new_user)
            try:
                next_match = resolve(google_form.cleaned_data['next_url'])
                return redirect(google_form.cleaned_data['next_url'])

            except:
                print(google_form.cleaned_data['next_url'])
                return redirect('base:index')

        else:
            print(google_form.errors)
            print("oops unclean data")
            return HttpResponse("Invalid data")

    else:
        return HttpResponse("Method GET not allowed")
