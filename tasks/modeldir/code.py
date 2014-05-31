from codejail.jail_code import jail_code, configure
from django.conf import settings
from common import models
from tasks.modeldir.base import Criteria, MarkedCriteria
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
    (10, 'That looks good to me!'),
    (8, 'Almost there, but check the whitespace (newlines, spaces, tabs).'),
    (5, 'Getting there, but check that the punctuation is correct.'),
    (3, 'Your answer looks right, but some letters aren\'t capitalised correctly.'),
    (0, 'Doesn\'t look right to me...'),
    (0, 'Your code timed out. It may have an infinite loop, or it may just be too slow.'),
    (0, 'Your code threw an error...'),
    (0, 'Unknown error')
]))

class CodeSubmission(Submission):
    class Meta:
        app_label = 'tasks'

    order = models.IntegerField()  # for code tasks, we can have multiple submissions
    # set this to null because we always create marked, but create after creating codesubmissions
    marked = models.ForeignKey(MarkedCriteria, null=True, blank=True)

    def on_submit(self, bonus):
        # here we execute their code
        code = bonus['data'].read().decode('UTF-8')
        submissions = CodeSubmission.objects.filter(user=self.user, task=self.task)
        self.order = max([x.order for x in submissions] + [0]) + 1
        marked = MarkedCode(desc=self.task.name, marks=10, max_marks=10)
        marked.save()
        self.marked = marked  # see https://code.djangoproject.com/ticket/8892 before changing

        worst = 0
        for io in self.task.codetask.get_io_files():
            infile = io.infile.read()
            expected = io.outfile.read().decode('UTF-8')
            output = jail_code('python3', code, stdin=infile)
            comment = check_output(output.stdout, expected, output.status)
            worst = max(worst, comment)
            self.marked.add_child(io.name, *SCORES[comment][1])

        self.marked.comment = SCORES[worst][1][1]
        self.marked.save()

        return '%s (%s / %s)' % (self.marked.comment, self.marked.marks, self.marked.max_marks)


class TestCase(models.Model):
    class Meta:
        app_label = 'tasks'

    name = models.CharField(max_length=50)
    task = models.ForeignKey(CodeTask)
    infile = models.FileField(verbose_name='Input File', upload_to='testcases')
    outfile = models.FileField(verbose_name='Output File', upload_to='testcases')
    hidden = models.BooleanField()
    order = models.IntegerField()

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


class MarkedCode(MarkedCriteria):
    class Meta:
        app_label = 'tasks'

    class MPTTMeta:
        order_by = 'desc'

    def add_child(self, name, score, comment):
        child = MarkedCode(parent=self, desc=name, marks=score, comment=comment, max_marks=10)
        child.save()
        self.marks = min(child.marks, self.marks)
