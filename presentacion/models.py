from django.db import models
from django.contrib.auth.models import User

from oauth2client.contrib.django_util.models import CredentialsField

# Create your models here.

class CredentialsModel(models.Model):
    user = models.OneToOneField(User)
    credential = CredentialsField()

class DriveCredentialsModel(models.Model):
    user = models.OneToOneField(User)
    credential = CredentialsField()

class Event(models.Model):
    summary = models.CharField(max_length=100)
    date = models.DateField()
