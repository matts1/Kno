from django.core.exceptions import ValidationError
from django import forms
from common.forms import ModelForm
from tasks.modeldir.assign import AssignSubmission
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

    def clean(self):
        task = Task.objects.filter(id=int(self.cleaned_data.get('taskid', 0))).first()
        submission = AssignSubmission.objects.filter(user=self.user, task=task).first()
        if task is None:
            raise ValidationError('task does not exist')
        elif task.kind == 'read':
            raise ValidationError('task is not submittable')
        elif task.course.students.filter(id=self.user.id).first() is None:
            raise ValidationError('You don\'t have permission to submit')
        elif submission is not None and submission.mark != 0:
            raise ValidationError('The task has already been marked')
        return self.cleaned_data

    def save(self):
        task = self.cleaned_data['taskid']
        if task.get_submission() == AssignSubmission:
            Submission.objects.filter(user=self.user, task=task).delete()  # 1 at a time
        self.text = task.get_submission().create(task, self.user, self.cleaned_data)
