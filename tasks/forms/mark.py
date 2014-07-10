from django.core.exceptions import ValidationError
from common.forms import ModelForm
from tasks.modeldir.assign import AssignSubmission


class MarkForm(ModelForm):
    class Meta:
        model = AssignSubmission
        fields = ('task',)

    def clean(self):
        if self.user != self.cleaned_data.get('task').course.teacher:
            raise ValidationError('You don\'t have permission')
        for key in self.data:
            splitted = key.split('_')
            if len(splitted) == 2 and splitted[0] == 'mark' and splitted[1].isdigit():
                student = int(splitted[1])
                if self.data[key][0].isdigit():
                    mark = int(self.data[key][0])
                    submission = AssignSubmission.objects.filter(
                        user=student,
                        task=self.cleaned_data['task']
                    ).first()
                    submission.mark = mark
                    submission.save()
        return self.cleaned_data
