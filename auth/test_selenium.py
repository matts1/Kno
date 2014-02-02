from common.selenium import SeleniumTestCase


class AuthTestCase(SeleniumTestCase):
    def test_register(self):
        self.browser.get(self.live_server_url)
        registerbtn = self.browser.find_element_by_css_selector(r'a[href=\#RegisterForm]')
        registerbtn.click()

