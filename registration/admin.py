from django.contrib import admin
from .models import EmailConfirmation, LastPasswordChange


admin.site.register(EmailConfirmation)
admin.site.register(LastPasswordChange)