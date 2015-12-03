import os
from django.db import models
from django.utils.deconstruct import deconstructible
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin, Permission)
from django.contrib.auth.models import Group as MasterGroup
from django.utils.translation import ugettext_lazy as _
from django.utils.html import format_html
from django.utils import timezone
from django.conf import settings
from wuser.storage import OverwriteStorage
from wuser.validators import national_id_validator


class Group(MasterGroup):
    pass


@deconstructible
class PathAndRename(object):
    def __init__(self, sub_path):
        self.path = sub_path

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        # set filename as random string
        filename = '{}.{}'.format(instance.id, ext)
        # return the whole path to the file
        return os.path.join(self.path, filename)


class UserManager(BaseUserManager):
    def create_user(self, national_id, first_name, last_name, email,
                    password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not national_id:
            raise ValueError('Users must provide a national id')

        user = self.model(national_id=national_id, first_name=first_name,
                          last_name=last_name, email=email)

        user.set_password(password)
        user.is_admin = False
        user.save(using=self._db)
        return user

    def create_superuser(self, national_id, first_name, last_name, email,
                         password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(national_id, first_name=first_name,
                                last_name=last_name, email=email,
                                password=password)
        user.is_admin, user.is_staff, user.is_superuser = True, True, True
        user.save(using=self._db)
        # user.confirm_email(user.confirmation_key)
        return user


path_and_rename = PathAndRename("avatars")


class User(AbstractBaseUser, PermissionsMixin):
    """
    main user class which inherit from AbstractBaseUser and implements some
    features.
    """
    national_id = models.CharField(_('National ID(username)'), max_length=10,
                                   unique=True,
                                   validators=[national_id_validator])
    first_name = models.CharField(_('First Name'), max_length=30)
    last_name = models.CharField(_('Last Name'), max_length=30)
    email = models.EmailField(_('Email'), )
    picture = models.ImageField(_('Profile Picture'), upload_to=path_and_rename,
                                storage=OverwriteStorage(), null=True,
                                blank=True)
    is_staff = models.BooleanField(_('Staff Status'), default=False, help_text=
    _('Designates whether the user can log into staff site.'))
    is_active = models.BooleanField(_('Active'), default=True, help_text=
    _('Designates whether this user should be treated as active. Unselect this '
      'instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('Date Joined'), default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'national_id'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']

    def get_full_name(self):
        """
        :return: the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """
        :return: the short name for the user.
        """
        return self.first_name

    @property
    def picture_url(self):
        """
        :return: the url of image profile for user
        """
        if self.picture:
            return self.picture.url
        else:
            return os.path.join(settings.MEDIA_URL, 'avatars/0.png')

    @property
    def thumbnail(self):
        """
        :return:the thumbnail html for 80x80 picture
        """
        return format_html('<img src="{}" class="img-thumbnail"'
                           ' width="80" height="80">', self.get_image_url)

    # thumbnail.short_description = _("Thumbnail")

    full_name = property(get_full_name)
    short_name = property(get_short_name)

    def __unicode__(self):
        return self.get_full_name()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')


# admin_user = User.objects.get(is_superuser=True)


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    fathers_name = models.CharField(_('Fathers Name'), max_length=30)
    birth_date = models.DateField(_('Birth Date'))
    phone_number = models.CharField(_('Phone Number'), max_length=20,
                                    null=True, blank=False)
    home_phone = models.CharField(_('Home Phone'), max_length=20, null=True,
                                  blank=True)
    home_address = models.TextField(_('Home Address'), max_length=100,
                                    null=True, blank=False)
    MALE = 1
    FEMALE = 2
    GENDER_CHOICES = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
    )
    gender = models.IntegerField(_('Gender'), choices=GENDER_CHOICES,
                                 null=True, blank=False)
    description = models.TextField(_('Description'), null=True, blank=True,
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
    acquaintance_way = models.IntegerField(
        _('How did you find "ela"?'), choices=ACQUAINTANCE_WAY_CHOICES,
        default=WEBSITE, null=True,
        blank=True)
