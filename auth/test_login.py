from django.core.urlresolvers import reverse
from django.test import TestCase
from auth.forms import LoginForm
from auth.models import Session


class LoginFormTest(TestCase):
    fixtures = ['auth']

    def test_bad_email(self):
        LoginForm.test(['email'],
            email='bademail',
            pwd='random'
        )

    def test_missing_email(self):
        LoginForm.test([''],  # raises an error to main form
            email='missingemail@gmail.com',
            pwd='random'
        )

    def test_bad_password(self):
        LoginForm.test([''],  # raises an error to main form
            email='student@gmail.com',
            pwd='wrong'
        )

    def test_valid(self):
        LoginForm.test([], save=False,
            email='student@gmail.com',
            pwd='a'
        )

class LoginLogoutTest(TestCase):
    fixtures = ['auth']

    def test_logged_out_to_logout(self):  # here they were never logged in
        logout = self.client.get(reverse('logout'))
        self.assertEqual(logout.url, 'http://testserver/')
        self.assertEqual(logout.status_code, 302)

    def test_login_logout(self):
        index = self.client.get(reverse('index'))
        self.assertIn('RegisterForm', str(index.content))
        self.assertEqual(len(Session.objects.all()), 0)

        request = self.client.post(reverse('login'), data={'email': 'student@gmail.com', 'pwd': 'a'})
        self.assertEqual(request.status_code, 200)
        self.assertEqual(len(Session.objects.all()), 1)
        index = self.client.get(reverse('index'))
        self.assertNotIn('RegisterForm', str(index.content))

        self.client.get(reverse('logout'))
        self.assertEqual(len(Session.objects.all()), 0)
