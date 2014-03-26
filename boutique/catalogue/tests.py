# -*- coding: utf-8 -*-

from django.test import TestCase
from .models import Product


class ProductTest(TestCase):
    def test_can_create_product(self):
        p = Product(title="Wicked product",
                    slug="wicked")
        self.assertIsNotNone(p)
