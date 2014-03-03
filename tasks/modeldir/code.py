from codejail.jail_code import jail_code, configure
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from common import models
from common.functions import makepath
from tasks.modeldir.programming import check_output
from tasks.models import Task, Submission
import os

configure('python3', settings.PYTHON_SANDBOX_PATH)

class CodeTask(Task):
    class Meta:
        app_label = 'tasks'

    @classmethod
    def create(cls, *args, **kwargs):
        val = super().create(*args, **kwargs)
        os.mkdir(val.get_path())
        return val

    def get_path(self, name=''):
        return makepath('codeio/{}/{}'.format(self.id, name))

    def get_io_files(self):
        files = os.listdir(self.get_path())
        return sorted(set(['.'.join(f.split('.')[:-1]) for f in files]))

    def has_io_files(self, name):
        return os.path.isfile(self.get_path(name + '.in'))

    def delete_io_files(self, name):
        path = self.get_path(name)
        default_storage.delete(path + '.in')
        default_storage.delete(path + '.out')

SCORES = list(enumerate([
    'That looks good to me!',
    'Almost there, but check the whitespace (newlines, spaces, tabs).',
    'Getting there, but check that the punctuation is correct.',
    'Your answer looks right, but some letters aren\'t capitalised correctly.',
    'Doesn\'t look right to me...',
    'Your code timed out. It may have an infinite loop, or it may just be too slow.',
    'Your code threw an error...',
    'Unknown error'
]))

class CodeSubmission(Submission):
    class Meta:
        app_label = 'tasks'

    comment = models.IntegerField(choices=SCORES)
    order = models.IntegerField()  # for code tasks, we can have multiple submissions

    def on_submit(self, bonus):
        # here we execute their code
        code = bonus['data'].read().decode('UTF-8')
        submissions = CodeSubmission.objects.filter(user=self.user, task=self.task)
        self.order = max([x.order for x in submissions] + [0]) + 1
        self.comment = 0
        for io in self.task.codetask.get_io_files():
            infile = open(makepath('codeio/{}/{}.in'.format(self.task.id, io))).read().encode('UTF-8')
            expected = open(makepath('codeio/{}/{}.out'.format(self.task.id, io))).read()
            output = jail_code('python3', code, stdin=infile)

            self.comment = max(self.comment, check_output(output.stdout, expected, output.status))

        return 'submitted a code task (order=%d, comment=%s)' % (self.order, self.get_comment_display())


class TestCase(models.Model):
    class Mate:
        app_label = 'tasks'

    task = models.ForeignKey(CodeTask)
    name = models.CharField(max_length=50)
    infile = models.FileField(verbose_name='Input File', upload_to='testcases')
    outfile = models.FileField(verbose_name='Output File', upload_to='testcases')
    hidden = models.BooleanField()
    order = models.IntegerField()
