# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static

admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^', include('brand.urls')),
                       url(r'^products/', include('catalogue.urls')),
                       url(r'^checkout/', include('checkout.urls')),

                       url(r'^admin/', include(admin.site.urls)),
                       )

if settings.DEBUG:
    # Add user (admin) uploaded images
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    # Add Django debug toolbar
    import debug_toolbar
    urlpatterns += patterns('',
                            url(r'^__debug__/', include(debug_toolbar.urls)),)
