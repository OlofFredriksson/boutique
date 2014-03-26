# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import Order


class OrderAdmin(admin.ModelAdmin):
    list_filter = ('created', 'total_price', 'paid', 'shipped')


admin.site.register(Order, OrderAdmin)
