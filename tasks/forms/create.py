from django import forms
from django.core.exceptions import ValidationError
from common.forms import ModelForm
from tasks.models import Task


CHOICES = (
    ('read', 'Reading'),
    ('code', 'Programming')
)

class CreateTaskForm(ModelForm):
    name = 'Create Task'
    urlname = 'createtask'
    valid_users = (2,)
    success_msg = 'Your task has been created'

    kind = forms.ChoiceField(choices=CHOICES, initial='read', label='Task Type')

    class Meta:
        model = Task
        fields = ('name', 'course', 'kind')

    def __init__(self, *args, **kwargs):
        initial = kwargs.get('initial', {})
        super().__init__(*args, **kwargs)

        # only show the courses the user teaches, label them correctly
        self.fields['course'].queryset = self.user.get_courses_taught()
        self.fields['course'].label_from_instance = lambda course: course.name

    def clean(self) -> dict:
        if Task.objects.filter(
                name=self.cleaned_data.get('name'),
                course=self.cleaned_data.get('course')):
            raise ValidationError('That name is taken')
        return self.cleaned_data

    def clean_name(self, name):
        return name.strip()

    def save(self):
        kwargs = self.cleaned_data
        kwargs['desc'] = 'This description is empty. You might want to add something to it.'
        kind = self.cleaned_data['kind']
        del kwargs['kind']

        # TODO: depending on kind of task, call a different class to create the task.
        Task(**kwargs).save()
