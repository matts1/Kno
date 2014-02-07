from django.conf.urls import patterns, url
from common.views import FormView
from courses.forms import CreateCourseForm
from courses.forms.join import JoinCourseForm
from courses.views import ListCourseView

urlpatterns = patterns('',
    url(r'^list$', ListCourseView.as_view(), name='listcourses'),

    url(r'^create$', FormView.as_view(form_class=CreateCourseForm), name='createcourse'),
    url(r'^join$', FormView.as_view(form_class=JoinCourseForm), name='joincourse'),
)
