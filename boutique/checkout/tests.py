# -*- coding: utf-8 -*-
import unittest
import re
from StringIO import StringIO

from django.core.management import call_command
from django.db import models
from django.test import TestCase
from freezegun import freeze_time
from mock import Mock

from .forms import OrderDetailsForm
from .middleware import CartMiddleware
from .models import Cart, Order
import context_processors


class DummyProduct(models.Model):
    price = models.PositiveIntegerField()


def create_cart():
    c = Cart()
    c.save()
    return c


def create_product(price=1):
    dummy = DummyProduct(price=price)
    dummy.save()
    return dummy


class CartTest(TestCase):
    def test_can_create_cart(self):
        cart = create_cart()

        self.assertIsNotNone(cart)

    def test_cart_is_empty(self):
        cart = create_cart()

        self.assertEqual(0, cart.number_of_items)

    def test_add_product(self):
        cart = create_cart()

        cart.add(create_product())

        self.assertEqual(1, cart.number_of_items)

    def test_add_multiple_products(self):
        cart = create_cart()

        cart.add(create_product())
        cart.add(create_product())
        cart.add(create_product())

        self.assertEqual(3, cart.number_of_items)

    def test_increase_quantity(self):
        cart = create_cart()
        product_a = create_product()
        product_b = create_product()

        cart.add(product_a)
        cart.add(product_b)
        cart.add(product_a)

        self.assertEqual(3, cart.number_of_items)
        self.assertEqual(2, cart.number_of_products)

    def test_iterate_cart_items(self):
        cart = create_cart()

        cart.add(create_product())
        cart.add(create_product())
        cart.add(create_product())

        for cart_item in cart.items.all():
            self.assertEqual(1, cart_item.product.price)

    def test_can_clear_cart(self):
        cart = create_cart()

        cart.add(create_product())
        cart.add(create_product())
        cart.add(create_product())

        self.assertEqual(3, cart.number_of_items)
        cart.clear()
        self.assertEqual(0, cart.number_of_items)

    def test_total_price(self):
        cart = create_cart()

        cart.add(create_product(100))
        cart.add(create_product(200))
        cart.add(create_product(200))

        self.assertEqual(500, cart.total_price)

    @unittest.skip("Need to mock session")
    def test_get_cart(self):
        request = Mock()
        request2 = Mock()

        cart = Cart.objects.for_request(request)
        cart_again = Cart.objects.for_request(request)
        cart2 = Cart.objects.for_request(request2)

        self.assertEqual(cart, cart_again)
        self.assertNotEqual(cart, cart2)

    def test_can_remove_from_cart(self):
        cart = create_cart()
        product_a = create_product()
        product_b = create_product()

        cart.add(product_a)
        cart.add(product_b)
        cart.add(product_a)

        self.assertEqual(cart.number_of_items, 3)
        cart.remove(product_a)
        self.assertEqual(cart.number_of_items, 2)


class ContextProcessorTest(TestCase):
    def test_context_processor(self):
        cart = Cart()
        request = Mock()
        request.cart = cart

        context = context_processors.cart(request)

        self.assertEqual(context['cart'], cart)


class CartMiddlewareTest(TestCase):
    def test_middleware(self):
        middleware = CartMiddleware()
        request = Mock()

        middleware.process_request(request)

        self.assertIsNotNone(request.cart)


class OrderDetailsFormTest(TestCase):
    def test_valid_form(self):
        form = OrderDetailsForm(data={'name': 'bob',
                                      'email': '',
                                      'birthday_year': '1970',
                                      'birthday_month': '12',
                                      'birthday_day': '24',
                                      'street': 'Seasame',
                                      'city': 'Wonderland',
                                      'postal_code': '12345'})
        self.assertTrue(form.is_valid())

    def test_too_young(self):
        form = OrderDetailsForm(data={'name': 'bob',
                                      'email': '',
                                      'birthday_year': '1997',
                                      'birthday_month': '12',
                                      'birthday_day': '24',
                                      'street': 'Seasame',
                                      'city': 'Wonderland',
                                      'postal_code': '12345'})
        self.assertFalse(form.is_valid())

    def test_postal_code_no_letters(self):
        form = OrderDetailsForm(data={'name': 'bob',
                                      'email': '',
                                      'birthday_year': '1970',
                                      'birthday_month': '12',
                                      'birthday_day': '24',
                                      'street': 'Seasame',
                                      'city': 'Wonderland',
                                      'postal_code': 'wicked'})
        self.assertFalse(form.is_valid())


class OrderTest(TestCase):
    def test_code_generation(self):
        code = Order.generate_code('bob', 4)
        regex = re.compile(r'[B|O]')
        self.assertEqual(4, len(code))
        self.assertTrue(regex.match(code))


class CartCleanupCommandTest(TestCase):
    def test_no_old_found(self):
        create_cart()
        create_cart()
        create_cart()

        initial_count = Cart.objects.all().count()
        self.assertEqual(3, initial_count)

        command_output = StringIO()
        call_command('cart_cleanup', stdout=command_output)

        self.assertEqual('Deleted 0 old cart objects\n', command_output.getvalue())

    def test_two_old_found(self):
        create_cart()

        freezer = freeze_time("2014-03-20 12:00:01")
        freezer.start()

        create_cart()
        create_cart()

        freezer.stop()

        command_output = StringIO()
        call_command('cart_cleanup', stdout=command_output)
        post_count = Cart.objects.all().count()

        self.assertEqual('Deleted 2 old cart objects\n', command_output.getvalue())
        self.assertEqual(1, post_count)
