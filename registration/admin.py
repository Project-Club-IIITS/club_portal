from django.contrib import admin
from .models import EmailConfirmation, UserProfile, GoogleAuth


admin.site.register(EmailConfirmation)
admin.site.register(UserProfile)
admin.site.register(GoogleAuth)
