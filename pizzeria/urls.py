from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.generic.simple import direct_to_template

from registration.views import register

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),

    # pizzeria urls
    url(r'^', include('order.urls')),

    # auth urls
    url(r'^accounts/register/$', register, {
            'backend': 'registration.backends.simple.SimpleBackend',
            'success_url': '/checkout/'
        },
        name='registration_register'),
    url(r'^accounts/register/closed/$', direct_to_template, {
            'template': 'registration/registration_closed.html'
        },
        name='registration_disallowed'),
    (r'^accounts/', include('registration.auth_urls')),
)
