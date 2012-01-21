from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Use simple registration urls to skip over email activation.
    url(r'^accounts/', include('registration.backends.simple.urls')),

    url(r'^', include('pizzeria.order.urls')),

)
