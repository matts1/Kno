from django import http
from django.conf import settings
from django.conf.urls import patterns, include, url

from django.contrib import admin
from django_jinja.views import GenericView
from common.views import TemplateView, get_user

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^auth/', include('auth.urls')),
    # url(r'^admin/', include(admin.site.urls)),

    url(r'^$', TemplateView.as_view(template_name='other/index.html'), name='index')
)

if settings.DEBUG == False:   #if DEBUG is True it will be served automatically
    urlpatterns += patterns('',
            url(
                r'^static/(?P<path>.*)$',
                'django.views.static.serve',
                {'document_root': settings.STATICFILES_DIRS[0]}
            ),
    )

class ErrorView(GenericView):
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
