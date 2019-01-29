from .models import Club


def clubs_processor(request):
    clubs = Club.objects.filter(is_active=True).exclude(name="clubs_portal")
    return {'clubs': clubs}
