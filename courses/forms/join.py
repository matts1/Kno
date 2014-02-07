from django.core.exceptions import ValidationError
from common.forms import ModelForm
from courses.models import Course

class JoinCourseForm(ModelForm):
    name = 'Join Course'
    urlname = 'joincourse'
    success_msg = 'You have joined the course'

    class Meta:
        model = Course
        fields = ('code',)

    def clean_code(self, code):
        self.course = Course.objects.filter(code=code)
        if not self.course.exists():
            raise ValidationError('The code was invalid')
        if self.course.first().teacher == self.user:
            raise ValidationError('You can\'t join a course you are teaching')
        if self.course.filter(students=self.user).exists():
            raise ValidationError('You are already in this course')
        self.course = self.course.first()

    def save(self):
        self.course.students.add(self.user)
        self.course.save()
