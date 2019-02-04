from .models import Club


def clubs_processor(request):
    clubs = Club.objects.filter(is_active=True).exclude(name__in=["clubs_portal", "Campus Life Committee"])
    return {'clubs': clubs}
