from django.shortcuts import redirect
from courses.views import ViewCourseView
from tasks.modeldir.base import Submission


class ScoreboardView(ViewCourseView):
    template_name = 'courses/scoreboard.html'
    valid_users = (1,)

    def get(self, request, *args, **kwargs):
        result = super().get(request, *args, **kwargs)
        if not self.permission:
            return redirect('index')
        return result

    def custom_context_data(self):
        mode = self.request.GET.get('mode', 'weighted')
        students = self.course.students.all()
        tasks = self.course.task_set.all().exclude(kind='read').order_by('id')
        totalweight = sum(x.weight for x in tasks)
        marks = {}
        total = 0
        for student in students:
            marks[student] = []
            total = 0
            for task in tasks:
                total += task.marks if mode == 'raw' else task.weight
                submission = task.get_submissions(student)
                if task.kind == 'assign':
                    mark = 0 if submission.first() is None else submission.first().mark
                elif task.kind == 'code':
                    mark = max(x.codesubmission.marked.marks for x in submission) / 10 * task.marks \
                        if submission else 0
                marks[student].append(mark if mode == 'raw' else (mark / task.marks * task.weight
                / totalweight))
            marks[student].append(sum(marks[student]))
        return {
            'course': self.course,
            'tasks': tasks,
            'students': sorted(students, key=lambda x: -marks[x][-1]),  # ordered by total marks desc
            'marks': marks,
            'mode': mode,
            'totalweight': totalweight,
            'totalmarks': total,
        }
