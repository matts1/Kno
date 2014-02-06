from auth.models import User
from common import models


class Course(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    code = models.CharField(max_length=20, null=True, blank=True)

    teacher = models.ForeignKey(User, related_name='taught')
    students = models.ManyToManyField(User, related_name='courses')
