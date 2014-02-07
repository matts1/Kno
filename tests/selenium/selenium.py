from selenium.common.exceptions import NoSuchElementException
from auth.models import User
from tests.base_selenium import SeleniumTestCase

class AuthTestCase(SeleniumTestCase):
    def test_register(self):
        self.browser.get(self.live_server_url)

        self.assertIsNone(User.get('a@b.com'))
        self.fill_form(
            'Register',
            {'email': 'a@b.com', 'pwd': 'abc', 'confpwd': 'abc', 'fname': 'bobby', 'lname': 'bob'},
            modal=True
        )
        self.fluent_wait(User.get, 'a@b.com', value=None, reverse=True)

    def test_login_logout(self):
        self.browser.get(self.live_server_url)

        self.fill_form(
            'Login',
            {'email': 'teacher@gmail.com', 'pwd': 'a'},
            modal=True
        )

        # check that we're logged in
        self.assertRaises(NoSuchElementException, self.fluent_wait,
            self.browser.find_element_by_id,
            'LoginForm'
        )

        # logout
        dropdown = self.browser.find_element_by_partial_link_text('Welcome')
        dropdown.click()

        logout_btn = self.browser.find_element_by_link_text(r'Logout')
        logout_btn.click()
