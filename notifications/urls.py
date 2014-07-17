from django.conf.urls import patterns, url
from notifications.views import NotifyView

urlpatterns = patterns('',
    url(r'^(\d+)$', NotifyView.as_view(), name='notify'),
)

