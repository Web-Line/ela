from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    fathers_name = models.CharField(_('fathers name'), max_length=30)
    birthdate = models.DateField(_('birthdate'))
    phone_number = models.CharField(_('phone number'), max_length=20,
                                    null=True, blank=False)
    home_phone = models.CharField(_('home phone'), max_length=20, null=True,
                                  blank=True)
    home_address = models.TextField(_('home address'), max_length=100,
                                    null=True, blank=False)
    MALE = 1
    FEMALE = 2
    GENDER_CHOICES = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
    )
    gender = models.IntegerField(_('gender'), choices=GENDER_CHOICES,
                                 null=True, blank=False)
    description = models.TextField(_('description'), null=True, blank=True,
                                   max_length=150)
    WEBSITE = 1
    TRAKT = 2
    FRIENDS = 3
    OTHER = 4
    ACQUAINTANCE_WAY_CHOICES = (
        (WEBSITE, 'Website'),
        (TRAKT, 'Trakt'),
        (FRIENDS, 'Friends'),
        (OTHER, 'Other')
    )
    acquaintance_way = models.IntegerField(_('witch connect you to ela'),
                                           choices=ACQUAINTANCE_WAY_CHOICES,
                                           default=WEBSITE, null=True,
                                           blank=True)