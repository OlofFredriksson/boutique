# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from .views import IndexView, TermsView, version_view


urlpatterns = patterns('',
    url(r'^$', IndexView.as_view(), name='home'),
    url(r'terms/$', TermsView.as_view(), name='terms'),
    url(r'version/$', version_view, name='version'),
)
