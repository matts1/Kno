from django import forms
from django.core.exceptions import ValidationError
from common.forms import ModelForm
from tasks.models import CodeTask, TestCase


class DeleteIOFileForm(ModelForm):
    name = 'Delete Test Case'
    urlname = 'deleteiofile'
    valid_users = (2,)

    class Meta:
        model = TestCase
        fields = ('task', 'name')

    def clean(self):
        if not TestCase.objects.filter(task=self.cleaned_data['task'],
                                       name=self.cleaned_data.get('name', '')):
            raise ValidationError('No test cases by that name')
        if self.cleaned_data['task'].course.teacher != self.user:
            raise ValidationError('Not enough permissions')
        return self.cleaned_data

    def clean_task(self, id):
        task = CodeTask.objects.filter(id=int(id)).first()
        if task is None:
            raise ValidationError('Task does not exist')
        elif task.course.teacher != self.user:
            raise ValidationError('You don\'t have permissions')
        return task

    def save(self):
        self.cleaned_data['task'].delete_io_files(self.cleaned_data['name'])


class AddIOFileForm(DeleteIOFileForm):
    name = 'Add Test Case'
    urlname = 'addiofile'
    valid_users = (2,)
    success_msg = 'Added file'

    # TODO: add a file size limit - see http://stackoverflow.com/questions/2894914/how-to-restrict-the-size-of-file-being-uploaded-apache-django/2895811#2895811

    class Meta:
        model = TestCase
        fields = ('task', 'name', 'infile', 'outfile')

    def clean(self):
        print(self.cleaned_data)
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
        ).save()
