from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from auth.models import User
from common import models
from courses.models import Course


TASK_TYPES = (
    ('read', 'Reading'),
    ('code', 'Programming'),
    ('assign', 'Assignment')
)


class Criteria(MPTTModel):
    class Meta:
        app_label = 'tasks'

    desc = models.CharField(max_length=400)
    parent = TreeForeignKey('self', null=True, blank=True)
    max_marks = models.IntegerField(blank=True)


class MarkedCriteria(Criteria):
    class Meta:
        app_label = 'tasks'

    marks = models.IntegerField(blank=True)
    comment = models.TextField()


# https://docs.djangoproject.com/en/1.6/topics/db/models/#multi-table-inheritance
# Task.objects.* can access subclasses of task as well as task
class Task(models.Model):
    class Meta:
        app_label = 'tasks'

    name = models.CharField(max_length=100)
    desc = models.CharField(max_length=10000)
    course = models.ForeignKey(Course)
    criteria = models.ForeignKey(Criteria, blank=True, null=True)
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

    def get_submissions(self, user):
        return self.get_submission().objects.filter(user=user, task=self)

    def get_submission(self):
        from tasks.models import CodeSubmission, AssignSubmission
        return {
            'read': Submission,
            'code': CodeSubmission,
            'assign': AssignSubmission
        }[self.kind]


class Submission(models.Model):
    class Meta:
        app_label = 'tasks'

    user = models.ForeignKey(User)
    task = models.ForeignKey(Task)
    criteria = models.ForeignKey(MarkedCriteria, null=True, blank=True)
    data = models.FileField(upload_to='submissions')

    def on_submit(self, bonus):
        return 'Your work has been submitted'

    @classmethod
    def create(cls, task, user, bonus):
        submission = cls(user=user, task=task, criteria=None, data=bonus['data'])
        msg = submission.on_submit(bonus)
        submission.save()
        return msg
