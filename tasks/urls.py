from django.conf.urls import patterns, url
from common.views import FormView
from tasks.forms import CreateTaskForm, EditTaskDescForm, AddIOFileForm, DeleteIOFileForm, SubmitForm
from tasks.forms.mark import MarkForm
from tasks.views.download import DownloadSubmissionView
from tasks.views.view import ViewTaskView

urlpatterns = patterns('',
    url(r'^view/(\d+)$', ViewTaskView.as_view(), name='viewtask'),
    url(r'^download/(\d+)/(.*)$', DownloadSubmissionView.as_view(), name='downloadsubmission'),

    url(r'^create$', FormView.as_view(form_class=CreateTaskForm), name='createtask'),
    url(r'^editdesc$', FormView.as_view(form_class=EditTaskDescForm), name='edittaskdesc'),
    url(r'^addiofile$', FormView.as_view(form_class=AddIOFileForm), name='addiofile'),
    url(r'^deleteiofile$', FormView.as_view(form_class=DeleteIOFileForm), name='deleteiofile'),
    url(r'^submit$', FormView.as_view(form_class=SubmitForm), name='submit'),
    url(r'^mark$', FormView.as_view(form_class=MarkForm), name='mark'),
)
