from auth.models import User
from common import models
from courses.models import Course


class BaseTask(models.Model):
    name = models.CharField(max_length=100)
    desc = models.CharField(max_length=10000)
    course = models.ForeignKey(Course)

    class Meta:
        abstract = True


class BaseSubmission(models.Model):
    user = models.ForeignKey(User)
    marks = models.IntegerField()
    # subclasses need to implement this to their own type of task
    # task = models.ForeignKey(BaseTask)

    class Meta:
        abstract = True
