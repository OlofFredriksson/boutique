# -*- coding: utf-8 -*-
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from ...models import Cart

DAYS_OLD_LIMIT = 2


class Command(BaseCommand):
    """
    Maintenance command used to remove old carts that are not used by an order.
    """
    def handle(self, *args, **options):
        try:
            qs = Cart.objects.filter(
                modified__lte=timezone.now()-timedelta(days=DAYS_OLD_LIMIT))

            count = qs.count()
            qs.delete()
            self.stdout.write('Deleted %s old cart objects' % count)
        except:
            self.stderr.write('Could not delete old cart objects')
