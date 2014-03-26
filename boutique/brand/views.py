# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.views.generic import TemplateView, View
from django.shortcuts import render_to_response

# These views should only be pure content views and must not not have any
# model dependencies.


class IndexView(TemplateView):
    template_name = 'index.html'


class TermsView(View):
    def get(self, request):
        return render_to_response('terms.html')


def version_view(request):
    return HttpResponse('Version: 1.0')

