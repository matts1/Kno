from django.core.exceptions import ValidationError
from django.test import TestCase
from auth.forms import RegisterForm


class RegisterFormTest(TestCase):
    def test_valid_form(self):
        RegisterForm.test({}, {'fname': 'John', 'lname': 'Smith'},
            email='john@smith.com',
            pwd='abc',
            confpwd='abc',
            fname='john',
            lname='smith'
        )

    def test_empty_form(self):
        RegisterForm.test({'email', 'pwd', 'confpwd', 'fname', 'lname'},
            email='',
            pwd='',
            confpwd='',
            fname='',
            lname=''
        )

    def test_bad_email(self):
        RegisterForm.test({'email'},
            email='j@s.',
            pwd='abc',
            confpwd='abc',
            fname='j',
            lname='s'
        )

    def test_bad_pwd(self):
        RegisterForm.test({''},
            email='j@s.co',
            pwd='abc',
            confpwd='abcd',
            fname='j',
            lname='s'
        )

    def test_valid(self):
        RegisterForm.test({}, {'fname': 'Bob', 'lname': 'Last'},
            email='j@s.co',
            pwd='abc',
            confpwd='abc',
            fname='bob',
            lname='last'
        )
