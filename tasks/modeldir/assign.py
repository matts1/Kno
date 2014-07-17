from django.core.urlresolvers import reverse
from common import models
from notifications.models import Notification
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
        sub = cls.objects.filter(user=user, task=task).first()
        if sub is None:
            sub = AssignSubmission(user=user, task=task, criteria=None, data=bonus['data'], mark=0)
        else:
            sub.data = bonus['data']
        sub.save()
        Notification.create(
            users=[task.course.teacher],
            heading='Task handed in',
            text='{} handed in for {}'.format(user.get_full_name(), task.name),
            url=reverse('viewtask', args=(task.id,))
        )
        return sub.on_submit(bonus)
