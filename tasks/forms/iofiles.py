from django import forms
from django.core.exceptions import ValidationError
from common.forms import ModelForm
from tasks.models import CodeTask


class DeleteIOFileForm(ModelForm):
    name = 'Delete Test Case'
    urlname = 'deleteiofile'
    valid_users = (2,)

    taskid = forms.IntegerField(min_value=0)
    ioname = forms.CharField(max_length=30, label='Name')

    class Meta:
        model = CodeTask
        fields = ('taskid', 'ioname')

    def clean(self):
        if not self.cleaned_data['taskid'].has_io_files(self.cleaned_data.get('ioname', '')):
            raise ValidationError('No test cases by that name')
        return self.cleaned_data

    def clean_taskid(self, id):
        task = CodeTask.objects.filter(id=int(id)).first()
        if task is None:
            raise ValidationError('Task does not exist')
        elif task.course.teacher != self.user:
            raise ValidationError('You don\'t have permissions')
        return task

    def save(self):
        print('saving')
        self.cleaned_data['taskid'].delete_io_files(self.cleaned_data['ioname'])


class AddIOFileForm(DeleteIOFileForm):
    name = 'Add Test Case'
    urlname = 'addiofile'
    valid_users = (2,)
    success_msg = 'Added file'

    # TODO: add a file size limit - see http://stackoverflow.com/questions/2894914/how-to-restrict-the-size-of-file-being-uploaded-apache-django/2895811#2895811
    infile = forms.FileField(allow_empty_file=True, label='Input File')
    outfile = forms.FileField(label='Output File')

    class Meta:
        model = CodeTask
        fields = ('taskid', 'ioname', 'infile', 'outfile')

    def clean(self):
        if self.cleaned_data['taskid'].has_io_files(self.cleaned_data.get('ioname', '')):
            raise ValidationError('A test case with that name already exists. If you want to '
                                  'overwrite it, please delete it first')
        return self.cleaned_data

    def save(self):
        self.cleaned_data['taskid'].add_io_files(
            self.cleaned_data['ioname'],
            self.cleaned_data['infile'],
            self.cleaned_data['outfile']
        )
