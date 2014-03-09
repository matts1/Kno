from django import forms
from django.core.exceptions import ValidationError
from common.forms import ModelForm
from tasks.models import TestCase


class DeleteIOFileForm(ModelForm):
    name = 'Delete Test Case'
    urlname = 'deleteiofile'
    valid_users = (1,)

    case = forms.IntegerField(label='case')

    class Meta:
        model = TestCase
        fields = ('case',)

    def clean_case(self, case):
        case = TestCase.objects.filter(id=int(case)).first()
        print(case)
        if case is None:
            raise ValidationError('No test case matching the id')
        if case.task.course.teacher != self.user:
            print(self.cleaned_data['case'].course.teacher)
            raise ValidationError('Not enough permissions')
        print(self.cleaned_data)
        return case

    def save(self):
        self.cleaned_data['case'].delete()


class AddIOFileForm(ModelForm):
    name = 'Add Test Case'
    urlname = 'addiofile'
    valid_users = (1,)
    success_msg = 'Added file'

    # TODO: add a file size limit - see http://stackoverflow.com/questions/2894914/how-to-restrict-the-size-of-file-being-uploaded-apache-django/2895811#2895811

    class Meta:
        model = TestCase
        fields = ('task', 'name', 'infile', 'outfile')

    def clean_task(self, task):
        if task is None:
            raise ValidationError('Task does not exist')
        elif task.course.teacher != self.user:
            raise ValidationError('You don\'t have permissions')
        return task

    def clean(self):
        if TestCase.objects.filter(task=self.cleaned_data['task'], name=self.cleaned_data.get(
            'name', '')):
            raise ValidationError('A test case with that name already exists. If you want to '
                                  'overwrite it, please delete it first')
        if self.cleaned_data['task'].course.teacher != self.user:
            raise ValidationError('Not enough permissions')
        return self.cleaned_data

    def save(self):
        TestCase(
            name=self.cleaned_data['name'],
            task=self.cleaned_data['task'],
            infile=self.cleaned_data['infile'],
            outfile=self.cleaned_data['outfile'],
            hidden=False,  # TODO: make user able to change this
            order=0,  # TODO: autoincrement this
        ).save()
