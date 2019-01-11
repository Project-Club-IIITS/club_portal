from django.shortcuts import render


# Create your views here.


def club_home(request):
    return render(request, 'clubs/index.html')
