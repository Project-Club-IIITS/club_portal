from django.shortcuts import render


# Create your views here.

def choose_club(request):
    return render(request, 'registration/choose-club.html')
