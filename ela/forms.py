from __future__ import unicode_literals
from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import authenticate, get_user_model
from django.utils.text import capfirst
from django.utils.translation import ugettext, ugettext_lazy as _
from rolepermissions.verifications import has_permission
from django.conf import settings
import logging

logger = logging.getLogger("ela")


class AuthenticationForm(forms.Form):
    """
    Base class for authenticating users. Extend this to get a form that accepts
    username/password logins.
    """
    username = forms.CharField(max_length=254)
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput)

    error_messages = {
        'invalid_login': _("Please enter a correct %(username)s and password. "
                           "Note that both fields may be case-sensitive."),
        'inactive': _("This account is inactive."),
    }

    def __init__(self, request=None, *args, **kwargs):
        """
        The 'request' parameter is set for custom auth use by subclasses.
        The form data comes in via the standard 'data' kwarg.
        """
        self.request = request
        self.user_cache = None
        super(AuthenticationForm, self).__init__(*args, **kwargs)

        # Set the label for the "username" field.
        UserModel = get_user_model()
        self.username_field = UserModel._meta.get_field(
            UserModel.USERNAME_FIELD)
        if self.fields['username'].label is None:
            self.fields['username'].label = capfirst(
                self.username_field.verbose_name)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            self.user_cache = authenticate(username=username,
                                           password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'username': self.username_field.verbose_name},
                )
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    def confirm_login_allowed(self, user):
        """
        Controls whether the given User may log in. This is a policy setting,
        independent of end-user authentication. This default behavior is to
        allow login by active users, and reject login by inactive users.

        If the given user cannot log in, this method should raise a
        ``forms.ValidationError``.

        If the given user may log in, this method should return None.
        """
        if not user.is_active:
            raise forms.ValidationError(
                self.error_messages['inactive'],
                code='inactive',
            )

    def get_user_id(self):
        if self.user_cache:
            return self.user_cache.id
        return None

    def get_user(self):
        return self.user_cache


class AdminPasswordChangeForm(PasswordChangeForm):
    required_css_class = 'required'


class MainAdminAuthenticationForm(AuthenticationForm):
    """
    A custom authentication form used in the admin app.
    """
    error_messages = {
        'invalid_login': _("Please enter the correct %(username)s and password "
                           "for a admin account. Note that both fields may be "
                           "case-sensitive."),
    }
    required_css_class = 'required'

    def confirm_login_allowed(self, user):
        logger.debug("attempt to login. user={}".format(user))

        if not user.is_active or not (user.is_superuser or user.is_staff):
            logger.debug("login blocked. user={}".format(user))
            raise forms.ValidationError(
                self.error_messages['invalid_login'],
                code='invalid_login',
                params={'username': self.username_field.verbose_name}
            )

        logger.debug("login is correct. user={}".format(user))


class StudentAdminAuthenticationForm(AuthenticationForm):
    """
    A custom authentication form used in the admin app. for students.
    """
    error_messages = {
        'invalid_login': _("Please enter the correct %(username)s and password "
                           "for a student account. Note that both fields may "
                           "be case-sensitive."
                           "If you sure, that %(username)s and password is "
                           "correct, your account might not activated yet, "
                           "or you don't have necessary privileges for "
                           "student account."),
    }
    required_css_class = 'required'

    def confirm_login_allowed(self, user):
        logger.debug("attempt to login. user={}".format(user))

        has_login_permission = has_permission(
            user,
            settings.LOGIN_STUDENT_ADMIN_SITE
        )
        if not user.is_active or not has_login_permission:
            logger.debug(
                "login blocked. user={}, has_login_permission={}".format(
                    user, has_login_permission
                )
            )
            raise forms.ValidationError(
                self.error_messages['invalid_login'],
                code='invalid_login',
                params={'username': self.username_field.verbose_name}
            )

        logger.debug("login is correct. user={}".format(user))


class TeacherAdminAuthenticationForm(AuthenticationForm):
    """
    A custom authentication form used in the admin app. for teachers.
    """
    error_messages = {
        'invalid_login': _("Please enter the correct %(username)s and password "
                           "for a teacher account. Note that both fields may "
                           "be case-sensitive."
                           "If you sure, that %(username)s and password is "
                           "correct, your account might not activated yet, "
                           "or you don't have necessary privileges for "
                           "teacher account."),
    }
    required_css_class = 'required'

    def confirm_login_allowed(self, user):
        logger.debug("attempt to login. user={}".format(user))

        has_login_permission = has_permission(
            user,
            settings.LOGIN_TEACHER_ADMIN_SITE
        )

        if not user.is_active or not has_login_permission:
            logger.debug(
                "login blocked. user={}, has_login_permission={}".format(
                    user, has_login_permission
                )
            )
            raise forms.ValidationError(
                self.error_messages['invalid_login'],
                code='invalid_login',
                params={'username': self.username_field.verbose_name}
            )

        logger.debug("login is correct. user={}".format(user))


class SupervisorAdminAuthenticationForm(AuthenticationForm):
    """
    A custom authentication form used in the admin app. for supervisor.
    """
    error_messages = {
        'invalid_login': _("Please enter the correct %(username)s and password "
                           "for a supervisor account. Note that both fields may "
                           "be case-sensitive."
                           "If you sure, that %(username)s and password is "
                           "correct, your account might not activated yet, "
                           "or you don't have necessary privileges for "
                           "supervisor account."),
    }
    required_css_class = 'required'

    def confirm_login_allowed(self, user):
        logger.debug("attempt to login. user={}".format(user))

        has_login_permission = has_permission(
            user,
            settings.LOGIN_SUPERVISOR_ADMIN_SITE
        )

        if not user.is_active or not has_login_permission:
            logger.debug(
                "login blocked. user={}, has_login_permission={}".format(
                    user, has_login_permission
                )
            )
            raise forms.ValidationError(
                self.error_messages['invalid_login'],
                code='invalid_login',
                params={'username': self.username_field.verbose_name}
            )

        logger.debug("login is correct. user={}".format(user))
