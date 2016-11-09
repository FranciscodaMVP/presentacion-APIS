from django.contrib import admin

from .models import CredentialsModel, Event
# Register your models here.

admin.site.register(CredentialsModel)
admin.site.register(Event)
