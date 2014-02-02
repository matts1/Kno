from auth.models import User
from common.selenium import SeleniumTestCase

class AuthTestCase(SeleniumTestCase):
    def test_register(self):
        self.browser.get(self.live_server_url)

        self.assertIsNone(User.get('a@b.com'))
        self.fill_form(
            'RegisterForm',
            {'email': 'a@b.com', 'pwd': 'abc', 'confpwd': 'abc', 'fname': 'bobby', 'lname': 'bob'},
            modal=True
        )
        self.fluent_wait(User.get, 'a@b.com', value=None, reverse=True)

    def test_login_logout(self):
        self.browser.get(self.live_server_url)

        self.fill_form(
            'LoginForm',
            {'email': 'student@gmail.com', 'pwd': 'a'},
            modal=True
        )

        # check that we're logged in

        # logout
