import sys

from django.test import LiveServerTestCase
from django.utils.importlib import import_module
from django.utils.unittest import SkipTest
from django.utils.translation import ugettext as _

class AdminSeleniumWebDriverTestCase(LiveServerTestCase):
    webdriver_class = 'selenium.webdriver.firefox.webdriver.WebDriver'

    @classmethod
    def setUpClass(cls):
        if sys.version_info < (2, 6):
            raise SkipTest('Selenium Webdriver does not support Python < 2.6.')
        try:
            # Import and start the WebDriver class.
            module, attr = cls.webdriver_class.rsplit('.', 1)
            mod = import_module(module)
            WebDriver = getattr(mod, attr)
            cls.selenium = WebDriver()
        except Exception:
            raise SkipTest('Selenium webdriver "%s" not installed or not '
                           'operational.' % cls.webdriver_class)
        super(AdminSeleniumWebDriverTestCase, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        super(AdminSeleniumWebDriverTestCase, cls).tearDownClass()
        if hasattr(cls, 'selenium'):
            cls.selenium.quit()

    def admin_login(self, username, password, login_url='/admin/'):
        """
        Helper function to log into the admin.
        """
        self.selenium.get('%s%s' % (self.live_server_url, login_url))
        username_input = self.selenium.find_element_by_name('username')
        username_input.send_keys(username)
        password_input = self.selenium.find_element_by_name('password')
        password_input.send_keys(password)
        login_text = _('Log in')
        self.selenium.find_element_by_xpath(
            '//input[@value="%s"]' % login_text).click()

    def get_css_value(self, selector, attribute):
        """
        Helper function that returns the value for the CSS attribute of an
        DOM element specified by the given selector. Uses the jQuery that ships
        with Django.
        """
        return self.selenium.execute_script(
            'return django.jQuery("%s").css("%s")' % (selector, attribute))