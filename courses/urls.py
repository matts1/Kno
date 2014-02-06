from django.conf.urls import patterns, url
from common.views import FormView
from courses.forms import CreateCourseForm

urlpatterns = patterns('',
    url(r'^create$', FormView.as_view(form_class=CreateCourseForm), name='createcourse'),
)
