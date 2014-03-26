# -*- coding: utf-8 -*-
import datetime
import re
from django import forms
from django.forms import extras
from django.utils.translation import ugettext_lazy as _

POSTAL_CODE_REGEX = re.compile('\d+')
YEARS = tuple(y for y in range(1920, 2000))


class OrderDetailsForm(forms.Form):
    """
    Form used to collect all required information when submitting an order.
    """
    name = forms.CharField()
    email = forms.EmailField(required=False)
    birthday = forms.DateField(widget=extras.SelectDateWidget(years=YEARS))
    street = forms.CharField()
    postal_code = forms.CharField()
    city = forms.CharField()

    def clean_birthday(self):
        birthday = self.cleaned_data['birthday']

        # Not a perfect solution given leap years but enough for demo!
        if birthday > datetime.datetime.now().date() - datetime.timedelta(days=18*365):
            raise forms.ValidationError(_('You need to be at least 18 years of age'))
        return birthday

    def clean_postal_code(self):
        postal_code = self.cleaned_data['postal_code']
        if not POSTAL_CODE_REGEX.match(postal_code):
            raise forms.ValidationError(_('Postal code can only contain digits'))
        return postal_code
