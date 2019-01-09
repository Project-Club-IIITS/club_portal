from django.contrib import admin
from .models import Club, ClubMember, ClubModerator, ClubPresident
# Register your models here.

admin.site.register(Club)
admin.site.register(ClubModerator)
admin.site.register(ClubMember)
admin.site.register(ClubPresident)

