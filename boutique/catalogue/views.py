# -*- coding: utf-8 -*-
from django.views.generic import ListView, DetailView
from .models import Beer


class ProductListView(ListView):
    context_object_name = 'products'
    template_name = 'product_list.html'
    paginate_by = 6

    def get_queryset(self):
        return Beer.objects.order_by('-modified')


class ProductDetailView(DetailView):
    template_name = 'product_detail.html'
    model = Beer
    context_object_name = 'product'
