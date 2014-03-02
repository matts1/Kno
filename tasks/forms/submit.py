from django.core.exceptions import ValidationError
from django import forms
from common.forms import ModelForm
from tasks.models import Submission, Task

class SubmitForm(ModelForm):
    name = 'Submit'
    urlname = 'submit'
    valid_users = (1,)
    success_msg = None  # write to self.text instead

    taskid = forms.IntegerField()

    class Meta:
        model = Submission
        fields = ('taskid', 'data')

    def clean_taskid(self, task):
        task = Task.objects.filter(id=int(task)).first()
        if task is None:
            raise ValidationError('task does not exist')
        elif task.kind == 'read':
            raise ValidationError('task is not submittable')
        elif task.course.students.filter(id=self.user.id).first() is None:
            raise ValidationError('You don\'t have permission to submit')
        return task

    def save(self):
        task = self.cleaned_data['taskid']
        self.text = task.get_submission().create(task, self.user, self.cleaned_data)
