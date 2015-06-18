from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('sales',
    url(r'^$', 'views.frontend'),
    url(r'^sales/$', 'views.adminpage'),
    url(r'^sales/uploadsprtvr/$', 'views.uploadsprtvr'),
    url(r'^sales/clearsprtvr/$',  'views.clearsprtvr'),
    url(r'^sales/uploadost/$',    'views.uploadost'),
    url(r'^sales/savenkl/$',      'views.savenkl'),
    url(r'^sales/delnkl/$',       'views.delnkl'),
)

