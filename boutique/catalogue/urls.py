# -*- coding: utf-8 -*-
from django.conf.urls import url, patterns
from .views import ProductListView, ProductDetailView

urlpatterns = patterns('',
    url(r'^$', ProductListView.as_view(), name="products_list"),
    url(r'^(?P<slug>[-\w]+)/$', ProductDetailView.as_view(), name="products_details"),
    )
