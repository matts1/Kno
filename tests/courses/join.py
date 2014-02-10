from courses.forms.join import JoinPublicCourseForm
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
        self.assertFalse(self.user() in course.students.all())
        JoinCourseForm.test(
            [],
            code=course.code,
            initdata={'user': self.user()}
        )
        self.assertTrue(self.user() in course.students.all())

class JoinPublicCourseTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user = lambda s, x='student@gmail.com': User.get(x)

    def test_no_id(self):
        JoinPublicCourseForm.test(
            ['courseid'],
            courseid=None,
            initdata={'user': self.user()}
        )

    def test_non_integer_id(self):
        JoinPublicCourseForm.test(
            ['courseid'],
            courseid='abcdef',
            initdata={'user': self.user()}
        )

    def test_bad_id(self):
        JoinPublicCourseForm.test(
            ['courseid'],
            courseid=9001,
            initdata={'user': self.user()}
        )

    def test_rejoin_course(self):
        course = Course.objects.get(pk='public course')
        JoinPublicCourseForm.test(
            ['courseid'],
            courseid=course.id,
            initdata={'user': self.user()}
        )

    def test_join_taught_course(self):
        course = Course.objects.get(pk='public course')
        JoinPublicCourseForm.test(
            ['courseid'],
            courseid=course.id,
            initdata={'user': self.user('teacher@gmail.com')}
        )

    def test_join_private(self):
        course = Course.objects.get(pk='my private course')
        JoinPublicCourseForm.test(
            ['courseid'],
            courseid=course.id,
            initdata={'user': self.user()}
        )

    def test_valid_join(self):
        course = Course.objects.get(pk='my public course')
        self.assertFalse(self.user() in course.students.all())
        JoinPublicCourseForm.test(
            [],
            courseid=course.id,
            initdata={'user': self.user()}
        )
        self.assertTrue(self.user() in course.students.all())
