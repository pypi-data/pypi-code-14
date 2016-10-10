from collections import Sequence

from bs4 import BeautifulSoup
from lazyutils import lazy
import selenium.webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Query(Sequence):
    def __init__(self, parent, elements):
        self.parent = parent
        self.elements = elements

    def click(self):
        """Clicks on all selected elements."""
        [x.click() for x in self]
        return self

    def __iter__(self):
        return iter(self.elements)

    def __len__(self):
        return len(self.elements)

    def __getitem__(self, i):
        return self.elements[i]


class IdManager:
    def __init__(self, driver):
        self.__dict__['_IdManager__driver'] = driver

    def __getattr__(self, id):
        return self[id]

    def __setattr__(self, id, value):
        self[id] = value

    def __getitem__(self, id):
        return self.__driver.find_element_by_id(id)

    def __setitem__(self, id, value):
        self[id].send_keys(value)


class WebDriverFacade:
    """
    A simplified interface to the selenium webdriver with simpler method names
    and a few useful resources.
    """

    soup_lib = 'html5lib'

    def __init__(self, driver, base_url='', wait=0, **kwargs):
        self._driver = driver
        self.base_url = base_url
        self.implicitly_wait(wait)
        for k, v in kwargs:
            if hasattr(self, k):
                setattr(self, k, v)
            else:
                raise TypeError('invalid argument: %r' % k)

    def __getattr__(self, attr):
        return getattr(self._driver, attr)

    def __call__(self, selector):
        elements = self.find_elements_by_css_selector(selector)
        return Query(self, [ElementFacade(x) for x in elements])

    def __getitem__(self, selector):
        return ElementFacade(self.find_element_by_css_selector(selector))

    @property
    def selenium(self):
        return self._driver

    @lazy
    def soup(self):
        """
        A beautiful soup interface to the HTML source code
        """

        return BeautifulSoup(self.html, self.soup_lib)

    @property
    def id(self):
        """
        A simplified interface to dom elements with a defined id.
        """

        return IdManager(self)

    def get(self, url=''):
        self.url = self.base_url + url
        return self._driver.get(self.base_url + url)

    def click(self, selector):
        """Clicks in the first element with the given CSS selector."""

        self[selector].click()

    def keys(self, *args):
        """Alias to send_keys()"""

        return self.send_keys(*args)

    # Wait conditions
    def wait_on(self, func, timeout=1.0):
        """Wait until func(driver) return True.

        Raises a TimeoutError if condition is not met in the given interval."""

        WebDriverWait(self, timeout).until(func)

    def wait_title_is(self, value, timeout=1.0):
        """Waits until the page title assumes the given value.

        Raises a TimeoutError if condition is not met in the given interval."""

        condition = EC.title_is(value)
        WebDriverWait(self, timeout).until(condition)

    def wait_title_contains(self, value, timeout=1.0):
        """Waits until the page title contains the given value.

        Raises a TimeoutError if condition is not met in the given interval."""

        condition = EC.title_contains(value)
        WebDriverWait(self, timeout).until(condition)


class ElementFacade:
    def __init__(self, element):
        self._element = element

    def fill(self, data):
        self.send_keys(data)

    def __getattr__(self, attr):
        return getattr(self._element, attr)


class Driver(WebDriverFacade):
    """
    The sulfur web driver.

    Args:
        driver:
            If given, can be a string or a Selenium webdriver object. The
            accept strings are: "firefox", "chromium".
    """
    def __init__(self, driver=None, **kwargs):
        if driver is None:
            driver = selenium.webdriver.Firefox()
        if isinstance(driver, str):
            driver_cls = get_driver_class_from_string()
            driver = driver_cls()
        super().__init__(driver, **kwargs)


def get_driver_class_from_string(name):
    """
    Select driver class from name.
    """

    mapping = {
        'firefox': 'selenium.webdriver.Firefox',
        'chrome': 'selenium.webdriver.Chrome',
        'ie': 'selenium.webdriver.Ie',
        'edge': 'selenium.webdriver.Edge',
        'opera': 'selenium.webdriver.Opera',
        'safari': 'selenium.webdriver.Safari',
        'blackberry': 'selenium.webdriver.BlackBerry',
        'phantomjs': 'selenium.webdriver.PhantomJS',
        'android': 'selenium.webdriver.Android',
    }

    mod, _, cls = mapping[name].rpartition('.')
    cls_list = __import__(mod, fromlist=[cls])
    return cls_list[0]