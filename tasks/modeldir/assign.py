from common import models
from tasks.modeldir.base import Task, Submission


class AssignTask(Task):
    class Meta:
        app_label = 'tasks'

class AssignSubmission(Submission):
    class Meta:
        app_label = 'tasks'

    mark = models.PositiveIntegerField(default=0)

    def on_submit(self, bonus):
        return 'Submitted'

    @classmethod
    def create(cls, task, user, bonus):
        submission = cls.objects.filter(user=user, task=task).first()
        if submission is None:
            msg = Submission.create(task, user, bonus)
        else:
            submission.data = bonus['data']
            msg = submission.on_submit(bonus)
            submission.save()
        return msg

