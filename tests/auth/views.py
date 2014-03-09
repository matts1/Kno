from auth.models import User
from tests.base_request import RequestTestCase


class AuthViewsTestCase(RequestTestCase):
    def test_profile(self):
        self.assertEqual(
            self.fetch('profile', User.objects.get(email='student@gmail.com').id).status_code,
            200
        )

    def test_settings(self):
        self.assertEqual(self.fetch('settings').status_code, 200)
