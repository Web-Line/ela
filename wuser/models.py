import os
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin, Permission)
from django.contrib.auth.models import Group as MasterGroup
from django.utils.translation import ugettext_lazy as _
from django.utils.html import format_html
from django.utils import timezone
from django.conf import settings
# from simple_email_confirmation import SimpleEmailConfirmationUserMixin

from wuser.storage import OverwriteStorage


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
        user.is_admin, user.is_staff, user.is_superuser  = True, True, True
        user.save(using=self._db)
        # user.confirm_email(user.confirmation_key)
        return user


path_and_rename = PathAndRename("avatars")


def national_id_validator(value):
    """
    Check if national_id is correct.
    :param value: national_id
    :type value: str
    :raises: ValidationError
    :returns: None
    """
    # We don't need validation when DEBUG is True.
    if settings.DEBUG:
        return

    if len(value) != 10:
        raise ValidationError(_('National ID most contain exactly 10 digits'))

    numbers_list = []
    result = 0
    for chars in value:
        try:
            numbers_list.append(int(chars))
        except:
            raise ValidationError(_('National ID must be numeric'))

    numbers_list = list(reversed(numbers_list))
    for i in range(len(numbers_list)):
        if i != 0:
            result += (i + 1) * numbers_list[i]

    if result % 11 < 2:
        control = result % 11
    else:
        control = 11 - (result % 11)
    if control != numbers_list[0]:
        raise ValidationError(_('Invalid National ID, Please make sure provided'
                                ' National ID is correct'))


class User(AbstractBaseUser, PermissionsMixin):
    """
    main user class which inherit from AbstractBaseUser and implements some
    features.
    """
    national_id = models.CharField(_('National ID(username)'), max_length=10,
                                   unique=True,
                                   validators=[national_id_validator])
    first_name = models.CharField(_('first name'), max_length=30)
    last_name = models.CharField(_('last name'), max_length=30)
    email = models.EmailField(_('email address'), )
    photo = models.ImageField(_('profile image'), upload_to=path_and_rename,
                              storage=OverwriteStorage(), null=True,
                              blank=True)
    is_staff = models.BooleanField(_('staff status'), default=False, help_text=
    _('Designates whether the user can log into staff site.'))
    is_active = models.BooleanField(_('active'), default=True, help_text=
    _('Designates whether this user should be treated as active. Unselect this '
      'instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'national_id'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']

    def get_full_name(self):
        """
        :return: the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()
    
    full_name = property(get_full_name)

    def get_short_name(self):
        """
        :return: the short name for the user.
        """
        return self.first_name

    def get_image_url(self):
        """
        :return: the url of image profile for user
        """
        if self.photo:
            return self.photo.url
        else:
            return os.path.join(settings.MEDIA_URL, 'avatars/0.png')

    def get_pic_html(self):
        """
        :return:the thumbnail html for 80x80 picture
        """
        return format_html('<img src="{}" class="img-thumbnail"'
                           ' width="80" height="80">', self.get_image_url)

    get_pic_html.short_description = _("Thumbnail")

    thumbnail = property(get_pic_html)

    def __unicode__(self):
        return self.get_full_name()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

# admin_user = User.objects.get(is_superuser=True)
