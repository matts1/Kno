from django.conf.urls import patterns, url
from common.views import FormView, TemplateView
from tasks.forms import CreateTaskForm

urlpatterns = patterns('',
    url(r'^create$', FormView.as_view(form_class=CreateTaskForm), name='createtask'),
)
