# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import Beer


class BeerAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'image', 'price', 'abv', 'created', 'modified')
    list_filter = ('created', 'title', 'abv')


admin.site.register(Beer, BeerAdmin)
