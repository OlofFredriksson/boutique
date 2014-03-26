# -*- coding: utf-8 -*-
import logging
from decimal import Decimal
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from model_utils.models import TimeStampedModel
from django.utils.translation import ugettext_lazy as _
from django.db import models

logger = logging.getLogger('django.request')


class CartManager(models.Manager):
    def for_request(self, request):
        if 'cart_id' in request.session:
            try:
                return self.get(pk=request.session['cart_id'])
            except ObjectDoesNotExist:
                pass

        return self.new_cart(request)

    def new_cart(self, request):
        cart = self.create()
        request.session['cart_id'] = cart.id
        return cart


class Cart(TimeStampedModel):
    # related: items (CartItem)
    objects = CartManager()

    class Meta:
        verbose_name = _('Cart')
        verbose_name_plural = _('Carts')

    @property
    def number_of_items(self):
        """
        Get the number of items (not products) in this cart.
        """
        list_of_quantities = self.items.all().values_list('quantity', flat=True)
        return sum(list_of_quantities)

    @property
    def number_of_products(self):
        """
        Get the list of different products in the cart.
        A product will count as (1) product regardless of quantity
        """
        return self.items.all().count()

    @property
    def total_price(self):
        total = 0
        for ci in self.items.all():
            total += ci.price
        return total

    def add(self, product):
        """
        Adds a product to the cart, if this product already exist in the cart
        the quantity will be incremented
        """
        try:
            item = self.items.get(product_object_id=product.id)
            item.quantity += 1
            item.save()
        except ObjectDoesNotExist:
            item = CartItem(cart=self, product=product, quantity=1)
            item.save()
        except Exception as e:
            logger.exception('Cannot add product to cart')

    def remove(self, product):
        """
        Removes a product to the cart, if this product contains more than one
        in quantity, the value will be decremented.
        """
        try:
            item = self.items.get(product_object_id=product.id)
            item.quantity -= 1
            if item.quantity < 1:
                item.delete()
            else:
                item.save()
        except Exception as e:
            logger.exception('No such product in cart')

    def clear(self):
        """
        Remove all cart items from the cart and save
        """
        CartItem.objects.filter(cart_id=self.id).delete()


class CartItem(models.Model):
    cart = models.ForeignKey(Cart,
                             related_name='items',
                             verbose_name=_('cart'))
    quantity = models.PositiveIntegerField()

    # Generic product relation
    product_content_type = models.ForeignKey(ContentType)
    product_object_id = models.PositiveIntegerField()

    class Meta:
        verbose_name = _('Cart item')
        verbose_name_plural = _('Cart items')

    @property
    def product(self):
        return self.product_content_type.get_object_for_this_type(
            pk=self.product_object_id)

    @product.setter
    def product(self, value):
        self.product_content_type = ContentType.objects.get_for_model(
            type(value))
        self.product_object_id = value.pk

    @property
    def price(self):
        return Decimal(self.product.price * self.quantity)

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('products_details', args=[str(self.product.slug)])

    def __unicode__(self):
        return "CartItem %s pcs %s" % (self.quantity, self.product.title)


class Order(TimeStampedModel):
    """
    The Order contains a reference to the Cart to contain the list of
    products.

    Pricing is kept local in the order to allow price changes.
    """
    code = models.CharField(max_length=16, unique=True, editable=False)
    name = models.CharField(max_length=255)
    email = models.EmailField(default='', blank=True)
    street = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=255)
    total_price = models.DecimalField(_('Price'), max_digits=12,
                                      decimal_places=2,
                                      default=Decimal('0.0'))
    paid = models.BooleanField(_('Paid'), default=False)
    shipped = models.BooleanField(_('Shipped'), default=False)
    cart = models.ForeignKey(Cart)

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')

    @staticmethod
    def generate_code(name, length=6):
        """
        Generate a (fairly) unique confirmation code based on users name.

        Not perfect, but this is only a demo.
        """
        import random
        return ''.join(random.choice(name) for _ in range(length)).upper()

    def __unicode__(self):
        return "Order %s" % (self.code,)
