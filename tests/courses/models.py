from courses.models import Course
from tests.base import TestCase


class ModelTestCase(TestCase):
    def test_list_tasks(self):
        self.assertEqual(len(Course.objects.get(name='private course').get_tasks()), 0)
        self.assertEqual(len(Course.objects.get(name='my public course').get_tasks()), 1)
