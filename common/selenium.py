from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait


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

    def wait_for_css(self, css_selector, timeout=7):
        """ Shortcut for WebDriverWait"""
        return WebDriverWait(self, timeout).until(lambda driver : driver.find_css(css_selector))

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
