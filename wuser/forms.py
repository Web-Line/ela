from django import forms
from django.forms.extras.widgets import SelectDateWidget
from django.utils.translation import ugettext_lazy as _
from wuser.models import UserProfile
from django.core.validators import RegexValidator
import account.forms
from wuser.validators import national_id_validator


class SignupForm(account.forms.SignupForm):
    national_id = forms.CharField(label=_('national ID (username)'),
                                  max_length=10,
                                  validators=[national_id_validator])
    photo = forms.ImageField(required=False)
    first_name = forms.CharField(required=True, max_length=30)
    last_name = forms.CharField(required=True, max_length=30)
    fathers_name = forms.CharField()
    gender = forms.ChoiceField(label=_('gender'),
                               choices=UserProfile.GENDER_CHOICES,
                               required=True)
    birth_date = forms.DateField(
        widget=SelectDateWidget(years=range(1910, 1991)))
    phone_number = forms.CharField(
        label=_('phone number'), validators=[RegexValidator(
            regex='^\d*$', message=_('not correct, only numbers'))],
        max_length=20, required=True)
    home_phone = forms.CharField(
        label=_('home phone'), validators=[RegexValidator(
            regex='^\d*$', message=_('not correct, only numbers'))],
        max_length=20)
    home_address = forms.CharField(label=_('home address'), max_length=100)
    acquaintance_way = forms.ChoiceField(
        label=_('acquaintance way'),
        choices=UserProfile.ACQUAINTANCE_WAY_CHOICES, required=True)
    description = forms.CharField(label=_('description'), max_length=150)
