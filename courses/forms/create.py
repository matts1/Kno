from django import forms
from common.forms import ModelForm
from common.validators import matches_regex
from courses.models import Course


class CreateCourseForm(ModelForm):
    name = 'Create Course'
    urlname = 'createcourse'
    valid_users = (2,)
    success_msg = 'Your course has been created'

    private = forms.BooleanField(label='Private', required=False)

    class Meta:
        model = Course
        fields = ('name', 'private', 'subject', 'year')

    clean_name = matches_regex(
        r'[\w\-]([\w\- ]+)?',
        'Enter a valid name (letters, numbers, hyphens and underscores)',
        lambda x: x.strip()
    )

    def save(self):
        Course.create(self.user, *[self.cleaned_data[x] for x in self.fields])
