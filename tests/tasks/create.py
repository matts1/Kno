from auth.models import User
from courses.models import Course
from tasks.forms import CreateTaskForm
from tests.base import TestCase

class CreateTaskTestCase(TestCase):
    def test_unowned_course(self):
        user = User.objects.get(email='teacher@gmail.com')
        course = Course.objects.get(name='my public course')
        CreateTaskForm.test(
            ['course'],
            initdata={'user': user},
            course=course,
            name='bad',
            kind='read',
        )

    def test_valid_and_duplicate_name(self):
        user = User.objects.get(email='teacher@gmail.com')
        CreateTaskForm.test(
            [],
            initdata={'user': user},
            course='public course',
            name=' good ',
            kind='read'
        )

    def test_duplicate_name(self):
        user = User.objects.get(email='mattstark75@gmail.com')
        CreateTaskForm.test(
            [''],
            initdata={'user': user},
            course='Programming',
            name='Programming Task 1',
            kind='code'
        )
