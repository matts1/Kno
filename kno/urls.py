from django.conf.urls import patterns, include, url, static

from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^auth/', include('auth.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('misc.urls')),
)
