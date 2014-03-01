from django.conf.urls import patterns, url
from common.views import FormView, TemplateView
from tasks.forms import CreateTaskForm
from tasks.views.view import ViewTaskView

urlpatterns = patterns('',
    url(r'^view/(\d+)$', ViewTaskView.as_view(), name='viewtask'),

    url(r'^create$', FormView.as_view(form_class=CreateTaskForm), name='createtask'),
)
