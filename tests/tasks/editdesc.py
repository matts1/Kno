from auth.models import User
from tasks.forms import EditTaskDescForm
from tasks.modeldir.base import Task
from tests.base import TestCase

class EditTaskDescTestCase(TestCase):
    def test_missing_task(self):
        user = User.objects.get(email='mattstark75@gmail.com')
        EditTaskDescForm.test(
            ['taskid'],
            initdata={'user': user},
            taskid=9001,
            desc='blah'
        )

    def test_wrong_teacher(self):
        user = User.objects.get(email='teacher@gmail.com')
        task = Task.objects.get(name='Task 1')
        EditTaskDescForm.test(
            ['taskid'],
            initdata={'user': user},
            taskid=task.id,
            desc='blah'
        )

    def test_student(self):
        user = User.objects.get(email='student@gmail.com')
        task = Task.objects.get(name='Task 1')
        EditTaskDescForm.test(
            ['taskid'],
            initdata={'user': user},
            taskid=task.id,
            desc='blah'
        )

    def test_valid(self):
        user = User.objects.get(email='mattstark75@gmail.com')
        task = Task.objects.get(name='Task 1')
        EditTaskDescForm.test(
            [],
            initdata={'user': user},
            taskid=task.id,
            desc='blah'
        )
