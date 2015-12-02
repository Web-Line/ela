from django import forms
from django.forms.extras.widgets import SelectDateWidget

import account.forms


class SignupForm(account.forms.SignupForm):
    fathers_name = forms.CharField()
    birthdate = forms.DateField(widget=SelectDateWidget(years=range(1910, 1991)))
