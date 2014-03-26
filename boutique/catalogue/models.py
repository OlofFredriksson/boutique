# -*- coding: utf-8 -*-
from decimal import Decimal
from django.db import models
from model_utils.models import TimeStampedModel
from django.utils.translation import ugettext_lazy as _


class Product(TimeStampedModel):
    title = models.CharField(_('Title'), max_length=255, blank=True)
    slug = models.SlugField(_('Slug'), max_length=255, unique=True)
    description = models.TextField(_('Description'), blank=True)
    image = models.ImageField(upload_to='product_images', default='images/missing.jpg')
    price = models.DecimalField(_('Price'), max_digits=12, decimal_places=2,
                                default=Decimal('0.0'))

    class Meta:
        abstract = True


class Beer(Product):
    abv = models.DecimalField(_('ABV %'), max_digits=12, decimal_places=2,
                              default=Decimal('0.0'))

    class Meta:
        verbose_name = _('Beer')
        verbose_name_plural = _('Beers')

    def __unicode__(self):
        return "Beer: %s" % self.title
