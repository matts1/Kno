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
    task = models.ForeignKey(BaseTask)
    marks = models.IntegerField()

    class Meta:
        abstract = True
