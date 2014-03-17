from django.shortcuts import get_object_or_404, redirect
from common.views import TemplateView, get_user
from tasks.modeldir.base import Task


class ViewTaskView(TemplateView):
    template_name = 'tasks/view.html'

    def get(self, request, *args, **kwargs):
        user = get_user(self)
        id = int(args[0])
        self.task = get_object_or_404(Task, id=id)
        return super().get(request, *args, **kwargs)

    def custom_context_data(self):
        return {'task': self.task}

