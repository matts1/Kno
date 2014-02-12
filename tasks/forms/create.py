from django import forms
from common.forms import ModelForm
from tasks.models.base import BaseTask


CHOICES = (
    ('read', 'Reading'),
    ('code', 'Programming')
)

class CreateTaskForm(ModelForm):
    name = 'Create Task'
    urlname = 'createtask'
    valid_users = (2,)

    kind = forms.ChoiceField(choices=CHOICES, initial='read', label='Task Type')

    class Meta:
        model = BaseTask
        fields = ('name', 'course', 'kind')

    def __init__(self, *args, **kwargs):
        initial = kwargs.get('initial', {})
        if kwargs['view'].__class__.__name__ == 'ViewCourseView':  # change the default value
            initial['course'] = kwargs['view'].course
            kwargs['initial'] = initial

        super().__init__(*args, **kwargs)
        # only show the courses the user teaches, label them correctly
        self.fields['course'].queryset = self.user.get_courses_taught()
        self.fields['course'].label_from_instance = lambda course: course.name
