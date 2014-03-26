# -*- coding: utf-8 -*-


def cart(request):
    """
    Make common cart properties available in the templates.
    """
    return {
        'cart': request.cart,
        'cart_count': request.cart.number_of_items
    }
