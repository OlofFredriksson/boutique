# -*- coding: utf-8 -*-
from django.conf.urls import url, patterns
from .views import (CartView, AddToCartActionView, ClearCartActionView,
                    RemoveFromCartActionView, OrderDetailsView, OrderConfirmationView)

urlpatterns = patterns('',
    # Checkout views
    url(r'^$', CartView.as_view(), name="cart"),
    url(r'^details/$', OrderDetailsView.as_view(), name="order_details"),
    url(r'^confirmation/$', OrderConfirmationView.as_view(), name="order_confirmation"),

    # Cart API
    url(r'^add/(?P<product_id>\d+)/$', AddToCartActionView.as_view(), name="cart_add"),
    url(r'^clear/$', ClearCartActionView.as_view(), name="cart_clear"),
    url(r'^remove/(?P<product_id>\d+)/$', RemoveFromCartActionView.as_view(), name="cart_remove"),
    )
