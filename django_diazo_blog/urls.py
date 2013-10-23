import os
from django.conf import settings
from django.conf.urls import patterns, include, url
import django_diazo_themes.angled_theme.view

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', django_diazo_themes.angled_theme.view.ExampleView.as_view(), name='home'),
    # url(r'^django_diazo_blog/', include('django_diazo_blog.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^%s/themes/(?P<path>.*)$' % settings.MEDIA_URL.strip('/'), 'django.views.static.serve',
            {'document_root': os.path.join(settings.MEDIA_ROOT, 'themes'), 'show_indexes': True}),
    )
