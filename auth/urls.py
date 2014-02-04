from django.conf.urls import patterns, url
from auth.forms import RegisterForm, LoginForm, ResetPwdForm, ForgotPwdForm, DoResetPwdForm
from auth.views import LogoutView, ProfileView
from common.views import FormView, TemplateView

urlpatterns = patterns('',
    url(r'^logout$', LogoutView.as_view(), name='logout'),
    url(r'^profile/(\d+)$', ProfileView.as_view(), name='profile'),

    url(r'^doreset/([0123456789abcdef]+)$', TemplateView.as_view(template_name='other/index.html'),
        name='doresetpwdview'),
    url(r'^settings$', TemplateView.as_view(template_name='user/settings.html'), name='settings'),

    url(r'^register$', FormView.as_view(form_class=RegisterForm), name='register'),
    url(r'^login$', FormView.as_view(form_class=LoginForm), name='login'),
    url(r'^reset$', FormView.as_view(form_class=ResetPwdForm), name='resetpwd'),
    url(r'^forgot$', FormView.as_view(form_class=ForgotPwdForm), name='forgotpwd'),
    url(r'^doresetform$', FormView.as_view(form_class=DoResetPwdForm), name='doresetpwd')
)
