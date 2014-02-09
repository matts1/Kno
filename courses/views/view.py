from django.shortcuts import get_object_or_404, redirect
from common.views import TemplateView, get_user
from courses.models import Course


class ViewCourseView(TemplateView):
    template_name = 'courses/view.html'
    valid_users = (1, 2)

    def get(self, request, *args, **kwargs):
        user = get_user(self)
        id = int(args[0])
        self.course = get_object_or_404(Course, id=id)
        if user is None or not user.can_see(self.course, Course):
            return redirect('index')
        return super().get(request, *args, **kwargs)

    def custom_context_data(self):
        return {'course': self.course}
