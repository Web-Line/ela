from django.conf import settings
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    fathers_name = models.CharField(max_length=30)
    birthdate = models.DateField()
