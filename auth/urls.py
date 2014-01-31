from django.conf.urls import patterns, url
from auth.forms import RegisterForm, LoginForm
from common.views import FormView

urlpatterns = patterns('',
    url(r'^login$', FormView.as_view(form_class=LoginForm), name='login'),
#    url(r'^logout$', 'logout', name='logout'),
    url(r'^register$', FormView.as_view(form_class=RegisterForm), name='register'),
#    url(r'^settings$', 'settings', name='settings'),
#    url(r'^forgot$', 'forgot', name='forgotpwd'),
#    url(r'^reset/(\d+)$', 'reset', name='resetpwd'),
#    url(r'^profile/(\d+))$', 'profile', name='profile'),
)
