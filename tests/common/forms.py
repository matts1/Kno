from django.core.urlresolvers import reverse
from tests.base import TestCase
from auth.forms import RegisterForm
from auth.models import User


class ModelFormTestCase(TestCase):
    def test_not_logged_in(self):
        self.assertTrue(RegisterForm().allowed(None))

    def test_student(self):
        self.assertFalse(RegisterForm().allowed(User.objects.get(email='student@gmail.com')))

    def test_teacher(self):
        self.assertFalse(RegisterForm().allowed(User.objects.get(email='teacher@gmail.com')))

    def test_as_form(self):
        self.assertEqual(RegisterForm(user=User.objects.get(email='teacher@gmail.com')).as_form(),
                         '')

    def test_less_errors(self):
        self.assertRaises(AssertionError, lambda: RegisterForm.test(['fname'],
            email='valid@gmail.com',
            pwd='abc',
            confpwd='abc',
            fname='valid',
            lname='valid'
        ))

    def test_extra_error(self):
        self.assertRaises(AssertionError, lambda: RegisterForm.test([],
            email='valid@gmail.com',
            pwd='abc',
            confpwd='abcdef',
            fname='valid',
            lname='valid'
        ))

    def test_wrong_cleaned_data(self):
        self.assertRaises(AssertionError, lambda: RegisterForm.test([],
            {'fname': 'first', 'lname': 'last'},
            email='valid@gmail.com',
            pwd='abc',
            confpwd='abc',
            fname='first',
            lname='last'
        ))

class MethodErrorTestCase(TestCase):
    def test_formview_get(self):
        self.assertEqual(self.client.get(reverse('login')).status_code, 405)

    def test_templateview_post(self):
        self.assertEqual(self.client.post(reverse('index')).status_code, 405)
