from django.conf.urls import patterns, url
from auth.forms import RegisterForm, LoginForm, ResetPwdForm
from auth.views import LogoutView
from common.views import FormView, TemplateView

urlpatterns = patterns('',
    url(r'^logout$', LogoutView.as_view(), name='logout'),
    url(r'^settings$', TemplateView.as_view(template_name='user/settings.html'), name='settings'),
#    url(r'^forgot$', 'forgot', name='forgotpwd'),

    url(r'^register$', FormView.as_view(form_class=RegisterForm), name='register'),
    url(r'^login$', FormView.as_view(form_class=LoginForm), name='login'),
    url(r'^reset$', FormView.as_view(form_class=ResetPwdForm), name='resetpwd'),
#    url(r'^profile/(\d+))$', 'profile', name='profile'),
)
