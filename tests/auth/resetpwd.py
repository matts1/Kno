from django.contrib.auth.hashers import check_password
from django.test import TestCase
from auth.forms import ResetPwdForm
from auth.models import User


class ResetPwdFormTest(TestCase):
    fixtures = ['auth']

    @classmethod
    def setUpClass(cls):
        # fixtures aren't set up yet, so this will return none unless we make it a function
        cls.user = lambda x: User.get('student@gmail.com')
        
    def test_empty_conf_pwd(self):
        ResetPwdForm.test(
            ['confpwd', ''],
            initdata={'user': self.user()},
            oldpwd='a',
            newpwd='blah',
            confpwd=''
        )

    def test_empty_new_pwd(self):
        ResetPwdForm.test(
            ['newpwd', ''],
            initdata={'user': self.user()},
            oldpwd='a',
            newpwd='',
            confpwd='blah'
        )

    def test_wrong_old_pwd(self):
        ResetPwdForm.test(
            [''],
            initdata={'user': self.user()},
            oldpwd='incorrect',
            newpwd='valid',
            confpwd='valid'
        )

    def test_different_new_pwd(self):
        ResetPwdForm.test(
            [''],
            initdata={'user': self.user()},
            oldpwd='a',
            newpwd='newpwd',
            confpwd='othernewpwd'
        )

    def test_valid_form(self):
        self.assertTrue(check_password('a', self.user().pwd))
        ResetPwdForm.test(
            [],
            initdata={'user': self.user()},
            oldpwd='a',
            newpwd='newpwd',
            confpwd='newpwd'
        )
        self.assertTrue(check_password('newpwd', self.user().pwd))
