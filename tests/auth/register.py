from django.core.urlresolvers import reverse
from auth.forms import RegisterForm
from tests.base import TestCase
from auth.models import User


class RegisterFormTest(TestCase):
    fixtures = ['data']

    def test_empty_form(self):
        RegisterForm.test(['email', 'pwd', 'confpwd', 'fname', 'lname'],
            email='',
            pwd='',
            confpwd='',
            fname='',
            lname=''
        )

    def test_bad_email(self):
        RegisterForm.test(['email'],
            email='j@s.',
            pwd='abc',
            confpwd='abc',
            fname='j',
            lname='s'
        )

    def test_bad_pwd(self):
        RegisterForm.test([''],
            email='j@s.co',
            pwd='abc',
            confpwd='abcd',
            fname='j',
            lname='s'
        )

    def test_email_taken(self):
        RegisterForm.test(['email'],
            email='student@gmail.com',
            pwd='pwd',
            confpwd='pwd',
            fname='taken',
            lname='blah'
        )

    def test_whitespace_fname(self):
        RegisterForm.test(['fname'],
            email='newaccount@gmail.com',
            pwd='pwd',
            confpwd='pwd',
            fname=' blah?',
            lname='ok'
        )

    def test_whitespace_lname(self):
        RegisterForm.test(['lname'],
            email='newaccount@gmail.com',
            pwd='pwd',
            confpwd='pwd',
            fname='ok',
            lname=' \n\t\r\f\v'
        )

    def test_valid(self):
        RegisterForm.test([], {'fname': 'John', 'lname': 'Smith'},
            email='john@smith.com',
            pwd='correcthorsebatterystaple',
            confpwd='correcthorsebatterystaple',
            fname='john',
            lname='smith'
        )
        user = User.get('john@smith.com')
        self.assertIsNotNone(user)
        self.assertEqual(user.fname, 'John')
        self.assertEqual(user.lname, 'Smith')
        self.assertEqual(user.get_short_name(), 'John')
        self.assertEqual(user.get_full_name(), 'John Smith')

    def test_valid2(self):
        RegisterForm.test([], {'fname': 'Bob', 'lname': 'Last'},
            email='j@s.co',
            pwd='abc',
            confpwd='abc',
            fname='bob',
            lname='last'
        )
        user = User.get('j@s.co')
        self.assertIsNotNone(user)
        self.assertEqual(user.fname, 'Bob')
        self.assertEqual(user.lname, 'Last')
        self.assertEqual(user.get_short_name(), 'Bob')
        self.assertEqual(user.get_full_name(), 'Bob Last')

    def test_view(self):
        self.assertIsNone(User.get('bob@gmail.com'))

        self.assertEqual(self.client.post(reverse('register'), dict(
            email='bob@gmail.com',
            pwd='mypwd',
            confpwd='mypwd',
            fname='bob',
            lname='student'
        )).status_code, 200)
        user = User.get('bob@gmail.com')
        self.assertIsNotNone(user)
        self.assertEqual(user.fname, 'Bob')
        self.assertEqual(user.lname, 'Student')
