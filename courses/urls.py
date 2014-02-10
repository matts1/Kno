from django.conf.urls import patterns, url
from common.views import FormView, TemplateView
from courses.forms import CreateCourseForm
from courses.forms import JoinCourseForm, JoinPublicCourseForm
from courses.views import ViewCourseView

urlpatterns = patterns('',
    url(r'^list$', TemplateView.as_view(template_name='courses/list.html'), name='listcourses'),
    url(r'^view/(\d+)$', ViewCourseView.as_view(template_name='courses/view.html'),
        name='viewcourse'),

    url(r'^create$', FormView.as_view(form_class=CreateCourseForm), name='createcourse'),
    url(r'^join$', FormView.as_view(form_class=JoinCourseForm), name='joincourse'),
    url(r'^joinpublic$', FormView.as_view(form_class=JoinPublicCourseForm),
        name='joinpubliccourse'),
)
