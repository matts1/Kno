from django.shortcuts import get_object_or_404
from common.views import TemplateView
from courses.models import Course


class ViewCourseView(TemplateView):
    template_name = 'courses/view.html'
    valid_users = (1, 2)

    def custom_context_data(self):
        id = int(self.args_data[0])
        return {'course': get_object_or_404(Course, id=id)}
