from django.conf.urls import patterns, include, url

from django.contrib import admin
from common.views import TemplateView

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^auth/', include('auth.urls')),
    # url(r'^admin/', include(admin.site.urls)),

    url(r'^$', TemplateView.as_view(template_name='other/index.html'), name='index')
)
