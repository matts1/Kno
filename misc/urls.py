from django.conf.urls import patterns, url
from misc.views import SearchView

urlpatterns = patterns('',
    url(r'^search$', SearchView.as_view(), name='search')
)
