from codejail.jail_code import jail_code, configure
from django.conf import settings
from common import models
from tasks.modeldir.programming import check_output
from tasks.models import Task, Submission

configure('python3', settings.PYTHON_SANDBOX_PATH)

class CodeTask(Task):
    class Meta:
        app_label = 'tasks'

    def get_io_files(self):
        return TestCase.objects.filter(task=self).order_by('name')

    def has_io_files(self, name):
        return TestCase.objects.filter(task=self, name=name).first() is not None

    def delete_io_files(self, name):
        TestCase.objects.get(name=name, task=self).delete()

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
            infile = io.infile.read()
            expected = io.outfile.read().decode('UTF-8')
            output = jail_code('python3', code, stdin=infile)

            self.comment = max(self.comment, check_output(output.stdout, expected, output.status))

        return 'submitted a code task (order=%d, comment=%s)' % (self.order, self.get_comment_display())


class TestCase(models.Model):
    class Meta:
        app_label = 'tasks'

    task = models.ForeignKey(CodeTask)
    name = models.CharField(max_length=50)
    infile = models.FileField(verbose_name='Input File', upload_to='testcases')
    outfile = models.FileField(verbose_name='Output File', upload_to='testcases')
    hidden = models.BooleanField()
    order = models.IntegerField()

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name
