from courses.models import Course
from tests.base import TestCase
from auth.models import User
from courses.forms import JoinCourseForm


class JoinCourseTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user = lambda s, x='student@gmail.com': User.get(x)

    def test_no_code(self):
        JoinCourseForm.test(
            ['code'],
            code=None,
            initdata={'user': self.user()}
        )

    def test_bad_code(self):
        JoinCourseForm.test(
            ['code'],
            code='abcdef',
            initdata={'user': self.user()}
        )

    def test_rejoin_course(self):
        course = Course.objects.get(pk='private course')
        JoinCourseForm.test(
            ['code'],
            code=course.code,
            initdata={'user': self.user()}
        )

    def test_join_taught_course(self):
        course = Course.objects.get(pk='private course')
        JoinCourseForm.test(
            ['code'],
            code=course.code,
            initdata={'user': self.user('teacher@gmail.com')}
        )

    def test_valid_join(self):
        course = Course.objects.get(pk='my private course')
        JoinCourseForm.test(
            [],
            code=course.code,
            initdata={'user': self.user()}
        )
