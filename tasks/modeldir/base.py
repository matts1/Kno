from auth.models import User
from common import models
from courses.models import Course


TASK_TYPES = (
    ('read', 'Reading'),
    ('code', 'Programming')
)

# https://docs.djangoproject.com/en/1.6/topics/db/models/#multi-table-inheritance
# Task.objects.* can access subclasses of task as well as task
class Task(models.Model):
    class Meta:
        app_label = 'tasks'

    name = models.CharField(max_length=100)
    desc = models.CharField(max_length=10000)
    course = models.ForeignKey(Course)
    kind = models.CharField(max_length=20, choices=TASK_TYPES, default='read', verbose_name='Task Type')

    @classmethod
    def create(cls, *args, **kwargs):
        task = cls(*args, **kwargs)
        task.save()

        from misc.models import Search  # bidirectional import
        Search.add_words(kwargs['name'], task.id, Task)
        return task

    def __repr__(self):
        return self.name

    def get_submission(self):
        from tasks.models import CodeSubmission
        return {
            'code': CodeSubmission
        }[self.kind]

class Submission(models.Model):
    class Meta:
        app_label = 'tasks'

    user = models.ForeignKey(User)
    marks = models.IntegerField()  # TODO: make this a seperate table for certain task types
    task = models.ForeignKey(Task)
    data = models.FileField(upload_to='submissions')

    def on_submit(self, bonus):
        return 'Your work has been submitted'

    @classmethod
    def create(cls, task, user, bonus):
        submission = cls(user=user, task=task, marks=-1, data=bonus['data'])
        msg = submission.on_submit(bonus)
        submission.save()
        return msg
