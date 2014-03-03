from django.core.exceptions import ValidationError
from django.forms import IntegerField
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
        self.course = Course.objects.filter(code=code.lower())
        if not self.course.exists():
            raise ValidationError('The code was invalid')
        self.course = self.course.first()
        if self.course.teacher == self.user:
            raise ValidationError('You can\'t join a course you are teaching')
        if self.user in self.course.students.all():
            raise ValidationError('You are already in this course')

    def save(self):
        self.course.students.add(self.user)
        self.course.save()

class JoinPublicCourseForm(ModelForm):
    name = 'Join Public Course'
    urlname = 'joinpubliccourse'
    success_url = 'viewcourse'
    success_url_args = lambda x: (x.course.id,)

    courseid = IntegerField(required=True)

    class Meta:
        model = Course
        fields = ('courseid',)

    def clean_courseid(self, id:str):
        self.course = Course.objects.filter(id=id)
        if not self.course.exists():
            raise ValidationError('The code was invalid')
        self.course = self.course.first()
        if self.course.code is not None:
            raise ValidationError('Course is not public')
        if self.course.teacher == self.user:
            raise ValidationError('You can\'t join a course you are teaching')
        if self.user in self.course.students.all():
            raise ValidationError('You are already in this course')

    def save(self):
        self.course.students.add(self.user)
        self.course.save()
