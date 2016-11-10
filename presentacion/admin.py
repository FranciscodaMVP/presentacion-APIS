from django.contrib import admin

from .models import CredentialsModel, DriveCredentialsModel, Event
# Register your models here.

admin.site.register(DriveCredentialsModel)
admin.site.register(CredentialsModel)
admin.site.register(Event)
