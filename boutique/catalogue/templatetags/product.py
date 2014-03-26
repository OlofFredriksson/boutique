# -*- coding: utf-8 -*-
from django import template

register = template.Library()

@register.filter
def percentage(value):
    return '%s %%' % (value,)

register.filter('percentage', percentage)
