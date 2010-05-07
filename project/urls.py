# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls.defaults import *


# Project URLs
# -----------------------------------------------------------------------------
urlpatterns = patterns('',
    url(r'^$',
        'django.views.generic.simple.direct_to_template', {
            'template': 'home/index.html',
        },
        name='home'
    )
)


# django.contrib.admin
# -----------------------------------------------------------------------------
if 'django.contrib.admin' in settings.INSTALLED_APPS:
    from django.contrib import admin
    admin.autodiscover()
    if 'django.contrib.admindocs' in settings.INSTALLED_APPS:
        urlpatterns += patterns('',
            url(r'^admin/doc/', 
                include('django.contrib.admindocs.urls')
            )
        )
    urlpatterns += patterns('',
        url(r'^admin/', 
            include(admin.site.urls)
        )
    )


# Static files
# -----------------------------------------------------------------------------
if settings.DEBUG:
    import re
    urlpatterns += patterns('django.views.static',
        url(r'^%s(?P<path>.*)$' % re.escape(settings.MEDIA_URL.lstrip('/')),
            'serve', {
                'document_root': settings.MEDIA_ROOT,
            }
        )
    )
