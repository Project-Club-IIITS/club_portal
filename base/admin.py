from django.contrib import admin
from .models import Club, ClubMember, ClubPresident, ClubModerator, ClubMentor, Notification

# Register your models here.

admin.site.register(Club)
admin.site.register(ClubMember)
admin.site.register(ClubPresident)
admin.site.register(ClubModerator)
admin.site.register(ClubMentor)
admin.site.register(Notification)