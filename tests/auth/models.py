from django.utils import timezone
from auth.models import Session, User
from courses.models import Course
from tasks.models import Task
from tests.base import TestCase


class ModelsTestCase(TestCase):
    def user(self):
        return self.lazy('student@gmail.com')

    def test_gravatar(self):
        self.assertEqual(
            self.user().gravatar(200),
            '<img src="http://www.gravatar.com/avatar/b8aeec8b91548b073d2b7e42f9d1328d?d=identicon&s=200" alt="gravatar">'
        )

    def test_pprint(self):
        self.assertEqual(self.user().pprint(), 'student@gmail.com')

    def test_str(self):
        self.assertEqual(repr(self.user()), 'student@gmail.com')

    def test_repr(self):
        self.assertEqual(str(self.user()), 'student@gmail.com')

    def test_sessions(self):
        id = Session.create(self.user())
        session = Session.get_user(id)
        self.assertEqual(session, self.user())

        session.expiry = timezone.now()
        session.save()
        Session.delete_old()

        self.assertIsNone(Session.get_user(session))

    def test_interaction(self):
        self.assertEqual(
            self.user().can_interact(User.objects.get(email='teacher@gmail.com'), User),
            True
        )

        self.assertEqual(
            self.user().can_interact(Course.objects.get(name='Programming'), Course), True
        )

        self.assertEqual(
            self.user().can_interact(Course.objects.get(name='my public course'), Course), False
        )

        self.assertEqual(
            self.user().can_interact(Task.objects.get(name='Programming Task 1'), Task), True
        )

        self.assertEqual(
            self.user().can_interact(Task.objects.get(name='my public course task 1'), Task), False
        )
