from django import forms
from django.core.exceptions import ValidationError
from common.forms import ModelForm
from tasks.models import Task

class EditTaskDescForm(ModelForm):
    name = 'Edit Task Description'
    urlname = 'edittaskdesc'
    valid_users = (1,)
    success_msg = 'Saved!'

    taskid = forms.IntegerField(min_value=0)

    class Meta:
        model = Task
        fields = ('desc', 'taskid')

    def clean_taskid(self, id):
        task = Task.objects.filter(id=int(id)).first()
        if task is None:
            raise ValidationError('Task does not exist')
        elif task.course.teacher != self.user:
            raise ValidationError('You don\'t have permissions')
        return task

    def save(self):
        task = self.cleaned_data['taskid']
        task.desc = self.cleaned_data['desc']
        task.save()
