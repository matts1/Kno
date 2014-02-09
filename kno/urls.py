from django import http
from django.conf import settings
from django.conf.urls import patterns, include, url

from django.contrib import admin
from django_jinja.views import GenericView
from common.views import TemplateView, get_user

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^auth/', include('auth.urls')),
    url(r'^courses/', include('courses.urls')),
    url(r'^misc/', include('misc.urls')),

    url(r'^$', TemplateView.as_view(template_name='other/index.html'), name='index')
)

class ErrorView(GenericView): # ensures that error templates are handled by jinja2, not django
    def get_context_data(self):  # copied from templateview so that we can render it properly
        kwargs = super().get_context_data()
        self.request.user = get_user(self)
        kwargs['info'] = (self, self.request.user)
        kwargs['user'] = self.request.user
        return kwargs

handler404 = ErrorView.as_view(
    response_cls = http.HttpResponseNotFound,
    tmpl_name='errors/404.html'
)
