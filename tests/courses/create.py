from tests.base import TestCase
from auth.models import User
from courses.forms import CreateCourseForm
from courses.models import Course


class CreateCourseTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user = lambda s, x='teacher@gmail.com': User.get(x)

    def test_empty_name(self):
        CreateCourseForm.test(
            ['name'],
            initdata={'user': self.user()},
            name='',
            private=False
        )

    def test_no_name(self):
        CreateCourseForm.test(
            ['name'],
            initdata={'user': self.user()},
            name=None,
            private=False
        )

    def test_student(self):
        self.assertEqual(CreateCourseForm.valid_users, (2,))

    def test_valid(self):
        CreateCourseForm.test(
            [],
            initdata={'user': self.user()},
            name='newname',
            private=False
        )
        course = Course.objects.filter(teacher=self.user()).first()
        self.assertIsNotNone(course)
        self.assertEqual(course.name, 'newname')
        self.assertEqual(course.code, None)

        # lets try creating another course under the same name
        CreateCourseForm.test(
            ['name'],
            initdata={'user': self.user()},
            name='newname',
            private=False
        )
