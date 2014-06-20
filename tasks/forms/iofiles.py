from zipfile import ZipFile
from django import forms
from django.conf import settings
from codejail.jail_code import jail_code, configure
from django.core.exceptions import ValidationError
from django.core.files.temp import NamedTemporaryFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from common.forms import ModelForm
from tasks.models import TestCase


configure('python3', settings.PYTHON_SANDBOX_PATH)


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
        if case is None:
            raise ValidationError('No test case matching the id')
        if case.task.course.teacher != self.user:
            raise ValidationError('Not enough permissions')
        return case

    def save(self):
        self.cleaned_data['case'].delete()


class AddIOFileForm(ModelForm):
    name = 'Set test cases'
    urlname = 'addiofile'
    valid_users = (1,)
    success_msg = 'Added test cases'

    program = forms.FileField(label='Correct program')
    zipfile = forms.FileField(label='Zipped input files')
    # TODO: add a file size limit - see http://stackoverflow.com/questions/2894914/how-to-restrict-the-size-of-file-being-uploaded-apache-django/2895811#2895811

    class Meta:
        model = TestCase
        fields = ('task', 'program', 'zipfile')

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
        program = self.cleaned_data['program'].read().decode('UTF-8')
        zipfile = ZipFile(self.cleaned_data['zipfile'])
        for name in zipfile.namelist():
            prefix = '.'.join(name.split('.')[:-1])
            zipfile.extract(name, 'media/zips')  # potential race condition
            inputfile = zipfile.open(name)
            output = jail_code('python3', program, stdin=inputfile.read()).stdout
            outfile = open('media/zips/testout', 'w')
            outfile.write(output.decode('UTF-8'))
            outfile.close()

            TestCase(
                name=prefix,
                task=self.cleaned_data['task'],
                infile=InMemoryUploadedFile(open('media/zips/' + name), 'infile', name, 'text/plain', len(inputfile.read()), None),
                outfile=InMemoryUploadedFile(open('media/zips/testout'), 'outfile', prefix + '.out', 'text/plain', len(output), None),
                hidden=False,  # TODO: make user able to change this
                order=0,  # TODO: autoincrement this
            ).save()
