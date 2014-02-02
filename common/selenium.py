from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
import time


class CustomWebDriver(webdriver.Firefox):
    def find_css(self, css_selector):
        """Shortcut to find elements by CSS. Returns either a list or singleton"""
        elems = self.find_elements_by_css_selector(css_selector)
        found = len(elems)
        if found == 1:
            return elems[0]
        elif not elems:
            raise NoSuchElementException(css_selector)
        return elems

class SeleniumTestCase(LiveServerTestCase):
    fixtures = ['auth']

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.browser = CustomWebDriver()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.browser.quit()

    def fluent_wait(self, function, *args, value=True, reverse=False, timeout=5, **kwargs):
        start = time.time()
        if not hasattr(value, '__call__'):
            cmp = lambda x: x == value

        while bool(cmp(function(*args, **kwargs))) == reverse:
            if time.time() - start > timeout:
                raise TimeoutError

    def fill_form(self, formname: str, data: dict, modal: bool=False):
        form = self.browser.find_element_by_css_selector('#' + formname)
        if modal:
            self.assertFalse(form.is_displayed())
            self.browser.find_element_by_css_selector(r'a[href=\#%s]' % formname).click()
            self.fluent_wait(form.is_displayed)

        for name, val in data.items():
            name = form.find_element_by_name(name)
            name.click()
            name.send_keys(val)

        submitbtn = form.find_element_by_css_selector('input.btn-primary')
        submitbtn.click()
