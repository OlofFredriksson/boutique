# -*- coding: utf-8 -*-
import logging

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
from django.views.generic import View, TemplateView, FormView

from .forms import OrderDetailsForm
from .models import Cart, Order
from catalogue.models import Beer


logger = logging.getLogger('django.request')


class AddToCartActionView(View):
    """
    Add a product to the cart.

    This is an action, so no result is rendered. On success a HTTP redirect
    is returned, on failure appropriate HTTP error.
    """
    def post(self, request, product_id):
        product = None
        try:
            product = Beer.objects.get(pk=product_id)
        except ObjectDoesNotExist:
            logger.warning('Trying to add non-existing product (pk=%s)' %
                           product_id)

        if product:
            cart = Cart.objects.for_request(request)
            cart.add(product)
            cart.save()

        return redirect('cart')


class RemoveFromCartActionView(View):
    """
    Removes one quantity for a product from the cart

    This is an action, so no result is rendered. On success a HTTP redirect
    is returned, on failure appropriate HTTP error.
    """
    def post(self, request, product_id):
        product = None
        try:
            product = Beer.objects.get(pk=product_id)
        except ObjectDoesNotExist:
            logger.warning('Trying to add non-existing product (pk=%s)' %
                           product_id)

        if product:
            cart = Cart.objects.for_request(request)
            cart.remove(product)
            cart.save()

        return redirect('cart')


class ClearCartActionView(View):
    """
    Clears the cart from all products (cart items) and save cart
    """
    def post(self, request):
        cart = Cart.objects.for_request(request)
        cart.clear()

        return redirect('products_list')


class CartView(TemplateView):
    """
    Cart view is the first view in the checkout. Presents the cart contents
    and options to alter that.
    """
    template_name = 'cart.html'


class OrderDetailsView(FormView):
    """
    The order details form where user enters final details. Form needs to be
    valid to leave this view
    """
    template_name = 'order_details.html'
    form_class = OrderDetailsForm

    def dispatch(self, request, *arg, **kwarg):
        """
        Make sure user has products in cart when visiting the checkout
        """
        if self.request.cart.number_of_items < 1:
            logging.debug('Accessing checkout without products')
            return redirect('home')
        return super(OrderDetailsView, self).dispatch(request, *arg, **kwarg)

    def form_valid(self, form):
        """
        This method is called when the form is submitted and all entered
        values validates OK.

        Responsible for creating and submitting the Order.
        """
        try:
            data = form.cleaned_data
            code = Order.generate_code(data['name'])
            cart = self.request.cart

            order = Order(code=code,
                          name=data['name'],
                          email=data['email'],
                          street=data['street'],
                          postal_code=data['postal_code'],
                          city=data['city'],
                          total_price=cart.total_price,
                          cart=cart)
            order.save()

            # Generate new cart for session. Old one must remain as it is
            # referred to from order
            self.request.cart = Cart.objects.new_cart(self.request)

            # Add confirmation code to session so that user can reload
            # confirmation page
            self.request.session['code'] = code
        except Exception as e:
            logging.exception('Could not create order')
            raise e
        return redirect('order_confirmation')


class OrderConfirmationView(TemplateView):
    template_name = 'order_confirmation.html'

    def dispatch(self, request, *arg, **kwarg):
        """
        Make sure user has products in cart when visiting the checkout
        """
        if not self.request.session.get('code'):
            logging.debug('Accessing checkout without products')
            return redirect('home')
        return super(OrderConfirmationView, self).dispatch(request, *arg, **kwarg)

    def get_context_data(self, **kwargs):
        """
        Hook used to add data to the template context available in the
        Django template (html)
        """
        context = super(OrderConfirmationView, self).get_context_data(**kwargs)
        context['code'] = self.request.session.get('code')
        return context
