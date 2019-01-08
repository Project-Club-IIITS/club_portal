from django.contrib import admin
from .models import EmailConfirmation, UserProfile


admin.site.register(EmailConfirmation)
admin.site.register(UserProfile)