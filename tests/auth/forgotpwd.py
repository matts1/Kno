from django.conf import settings
from django.contrib.auth.hashers import check_password
from django.test import TestCase
import time
from auth.forms import ForgotPwdForm, DoResetPwdForm
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

    def test_no_code(self):
        self.assertIsNone(User.get('student@gmail.com').reset_code)
        DoResetPwdForm.test(
            ['reset_code'],
            reset_code=None,
            pwd='abc',
            confpwd='abc'
        )

    def test_wrong_code(self):
        user = User.get('student@gmail.com')
        user.reset_code = 'code'
        user.save()
        DoResetPwdForm.test(
            ['reset_code'],
            reset_code='invalid',
            pwd='abc',
            confpwd='abc'
        )

    def test_diff_pwd(self):
        user = User.get('student@gmail.com')
        user.reset_code = 'code'
        user.save()
        DoResetPwdForm.test(
            [''],
            reset_code='code',
            pwd='abcd',
            confpwd='abc'
        )

    def test_no_pwd(self):
        user = User.get('student@gmail.com')
        user.reset_code = 'code'
        user.save()
        DoResetPwdForm.test(
            ['pwd', 'confpwd'],
            reset_code='code',
            pwd=None,
            confpwd=None
        )

    def test_empty_pwd(self):
        user = User.get('student@gmail.com')
        user.reset_code = 'code'
        user.save()
        DoResetPwdForm.test(
            ['pwd', 'confpwd'],
            reset_code='code',
            pwd='',
            confpwd=''
        )

    def test_valid(self):
        user = User.get('student@gmail.com')
        user.reset_code = 'code'
        user.save()
        DoResetPwdForm.test(
            [],
            reset_code='code',
            pwd='newpwd',
            confpwd='newpwd'
        )
        user = User.get('student@gmail.com')
        self.assertIsNone(user.reset_code)
        self.assertFalse(check_password('a', user.pwd))
        self.assertTrue(check_password('newpwd', user.pwd))
