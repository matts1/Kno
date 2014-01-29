from django.conf.urls import patterns, include, url, static

from django.contrib import admin
from django.views.generic import TemplateView

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^auth/', include('auth.urls')),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', TemplateView.as_view(template_name='other/index.html'), name='index')
)
