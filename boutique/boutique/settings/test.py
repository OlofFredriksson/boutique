# -*- coding: utf-8 -*-
from __future__ import absolute_import

from .base import *

ALLOWED_HOSTS = ['localhost']

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
        "USER": "",
        "PASSWORD": "",
        "HOST": "",
        "PORT": "",
    },
}
