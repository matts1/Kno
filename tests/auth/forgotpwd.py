from django.conf import settings
from django.test import TestCase
from auth.forms import ForgotPwdForm
from auth.models import User


class ForgotPwdFormTest(TestCase):
    fixtures = ['auth']

    @classmethod
    def setUpClass(cls):
        settings.TEST = True  # so it doesn't send email or print it out to console

    def test_invalid_email(self):
        ForgotPwdForm.test(['email'], email='blah')

    def test_missing_email(self):
        ForgotPwdForm.test([''], email='missing@blah.com')

    def test_valid_email(self):
        user = lambda: User.get('student@gmail.com')
        self.assertIsNone(user().reset_code)
        ForgotPwdForm.test([], email=user().email)
        self.assertIsNotNone(user().reset_code)
