from django.shortcuts import get_object_or_404, redirect
from common.views import TemplateView, get_user
from tasks.modeldir.assign import AssignSubmission
from tasks.modeldir.base import Task


class ViewTaskView(TemplateView):
    template_name = 'tasks/view.html'

    def get(self, request, *args, **kwargs):
        user = get_user(self)
        id = int(args[0])
        self.task = get_object_or_404(Task, id=id)
        self.submissions = {}
        if self.task.kind == 'assign' and self.task.course.teacher == user:
            for user in self.task.course.students.all():
                self.submissions[user] = AssignSubmission.objects.filter(
                    user=user,
                    task=self.task,
                ).first()
        return super().get(request, *args, **kwargs)

    def custom_context_data(self):
        return {
            'task': self.task,
            'students': self.submissions,
            'studentslist': sorted(self.submissions, key=lambda x: (x.lname, x.fname))
        }

