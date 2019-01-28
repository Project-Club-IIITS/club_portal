from .models import Club


def clubs_processor(request):
    clubs = Club.objects.all()
    return {'clubs': clubs}
