# -*- coding: utf-8 -*-
from django.utils.functional import SimpleLazyObject
from .models import Cart


class CartMiddleware(object):
    """
    Middleware responsible to assign cart to request. Assigning is lazy so DB
    will only be queried if someone actually access cart
    """
    def process_request(self, request):
        request.cart = SimpleLazyObject(
            lambda: Cart.objects.for_request(request)
        )
