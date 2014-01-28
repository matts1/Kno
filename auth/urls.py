from django.conf.urls import patterns, url

urlpatterns = patterns('auth.views',
    url(r'^login$', 'login', name='login'),
    url(r'^logout$', 'logout', name='logout'),
    url(r'^register$', 'register', name='register'),
    url(r'^settings$', 'settings', name='settings'),
    url(r'^forgot$', 'forgot', name='forgotpwd'),
    url(r'^reset/(\d+)$', 'reset', name='resetpwd'),
    url(r'^profile/(\d+))$', 'profile', name='profile'),
)
