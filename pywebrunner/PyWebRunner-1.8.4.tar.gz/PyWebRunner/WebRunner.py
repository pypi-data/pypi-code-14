from ast import literal_eval
from functools import partial
from time import sleep
from random import random
import importlib
# import base64
import logging
import os
import sys
import pkg_resources
import re
from PyWebRunner.utils import which, Timeout, fix_firefox, fix_chrome
from xvfbwrapper import Xvfb
from selenium import webdriver
from selenium.common.exceptions import (NoSuchElementException, NoSuchWindowException,
                                        NoAlertPresentException, WebDriverException,
                                        TimeoutException)
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.remote_connection import LOGGER as s_logger
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class WebRunner(object):
    """
    WebRunner runs an instance of Selenium and adds a lot of helpful
    browser methods.

    Generally this class aims to make the experience of using Selenium
    better overall.

    Many functions take a "selector" argument.
    These can be any valid CSS selector..
    See https://developer.mozilla.org/en-US/docs/Web/Guide/CSS/Getting_started/Selectors
    """
    # Variables for configuration
    browser = None
    extra_verbose = False
    silence = open(os.devnull, 'w')

    def __init__(self, **kwargs):
        self.base_url = kwargs.get('base_url', 'http://127.0.0.1:5000')
        self.root_path = kwargs.get('root_path', './')
        xvfb = kwargs.get('xvfb', True)
        driver = kwargs.get('driver', 'Chrome')
        mootools = kwargs.get('mootools', False)
        errors = kwargs.get('errors', False)
        timeout = kwargs.get('timeout', 90)
        width = kwargs.get('width', 1440)
        height = kwargs.get('height', 1200)
        desired_capabilities = kwargs.get('desired_capabilities', 'CHROME')
        command_executor = kwargs.get('command_executor', 'http://127.0.0.1:4444/wd/hub')

        if driver == 'Firefox':
            print('=' * 80)
            print("*** WARNING ***")
            print('=' * 80)
            print('You are using "Firefox" as your driver which is only compatible with')
            print('Firefox < 48.0.0 - This is probably the wrong driver. You are probably')
            print('looking for "Gecko" which uses the Mozilla geckodriver under the hood.')
            print("If you know what you are doing it is safe to ignore this warning.")
            print('=' * 80)
        elif driver == 'Gecko':
            print('=' * 80)
            print("*** WARNING ***")
            print('=' * 80)
            print('The "Gecko" driver is currently in a bad place and might not work as')
            print('expected. I have tried to work around its limitations automatically')
            print('but I still recommend that you use Chrome / chromedriver or Firefox 47')
            print('for now.')

        # Chrome, Firefox, Gecko, PhantomJS, Etc... (Must be installed...)
        self.driver = os.environ.get('WR_DRIVER', driver)
        # This is for headless running.
        self.xvfb = os.environ.get('WR_XVFB', xvfb)
        # Use MooTools instead of jQuery
        self.mootools = os.environ.get('WR_MOOTOOLS', mootools)
        # Global timeout option for all wait_* functions
        self.timeout = os.environ.get('WR_TIMEOUT', timeout)
        # XVFB virtual monitor width
        self.width = os.environ.get('WR_WIDTH', width)
        # XVFB virtual monitor width
        self.height = os.environ.get('WR_HEIGHT', height)
        self.js_errorcollector = True

        self.desired_capabilities = os.environ.get(
            'WR_DESIRED_CAPABILITIES', desired_capabilities)
        self.command_executor = os.environ.get(
            'WR_COMMAND_EXECUTOR', command_executor)

        self.yaml_funcs = {}
        self.yaml_vars = {}

        if os.environ.get('skip_xvfb'):
            self.xvfb = False

        # Turn off annoying selenium logs
        s_logger.setLevel(logging.WARNING)

    def _before(self):
        pass

    def start(self):
        """Starts Selenium and (optionally) starts XVFB first.

        Note:

            XVFB is typically used with headless runs. If you do not use XVFB
            and the browser you have selected has a GUI (Firefox, Chrome...)
            then your browser will launch and you will be able to view the
            test as it is being ran.

            This is particularly useful for problematic test runs or when building
            new tests.

        """
        if self.xvfb:
            try:
                print("\nStarting XVFB display...")
                self.display = Xvfb(width=self.width, height=self.height, colordepth=16)
                try:
                    self.display.start()
                except OSError:
                    self.xvfb = False
                    print("\nUnable to start XVFB. Try running `./build/selenium.sh`")
            except EnvironmentError:
                print("\nSkipping XVFB run since it is not present.")
                self.xvfb = False

        print("\nStarting browser ({})...".format(self.driver))

        if self.driver == "PhantomJS":
            self.browser = webdriver.PhantomJS()
        elif self.driver == "Chrome":
            if not which('chromedriver'):
                fix_chrome()

            from selenium.webdriver.chrome.options import Options
            chrome_options = Options()
            try:
                extension = pkg_resources.resource_filename('PyWebRunner', "../../../../extensions/JSErrorCollector.crx")
                chrome_options.add_extension(extension)
            except IOError:
                self.js_errorcollector = False

            self.browser = webdriver.Chrome(chrome_options=chrome_options)
        elif self.driver == "Opera":
            self.browser = webdriver.Opera()
        elif self.driver == "Ie":
            self.browser = webdriver.Ie()
        elif self.driver == "Remote":
            if isinstance(self.desired_capabilities, dict):
                dc = self.desired_capabilities
            else:
                dcu = self.desired_capabilities.upper()

                if dcu == 'IE':
                    dcu = 'INTERNETEXPLORER'

                dc = getattr(DesiredCapabilities, dcu)

            self.browser = webdriver.Remote(
                command_executor=self.command_executor,
                desired_capabilities=dc
            )

        elif self.driver in ('Firefox', 'Gecko'):
            # Get rid of the annoying start page by setting preferences
            fp = webdriver.FirefoxProfile()
            # Download from: https://github.com/mguillem/JSErrorCollector/raw/master/dist/JSErrorCollector.xpi
            try:
                extension = pkg_resources.resource_filename('PyWebRunner', "../../../../extensions/JSErrorCollector.xpi")
                fp.add_extension(extension)
            except IOError:
                self.js_errorcollector = False
            fp.set_preference("browser.startup.homepage_override.mstone", "ignore")
            fp.set_preference("startup.homepage_welcome_url.additional", "about:blank")
            if self.driver == 'Gecko':
                if which('wires') or which('geckodriver'):
                    caps = DesiredCapabilities.FIREFOX
                    caps['marionette'] = True
                    self.browser = webdriver.Firefox(firefox_profile=fp, capabilities=caps)
                else:
                    print('"wires" or "geckodriver" not found in path. Exiting.')
                    sys.exit(1)
            else:
                # self.browser = webdriver.Firefox(firefox_profile=fp)
                try:
                    with Timeout(8):
                        self.browser = webdriver.Firefox(firefox_profile=fp)
                except (Timeout.Timeout, WebDriverException):
                    if not self.browser:
                        fix_firefox()

                        if which('wires') or which('geckodriver'):
                            caps = DesiredCapabilities.FIREFOX
                            caps['marionette'] = True
                            self.browser = webdriver.Firefox(firefox_profile=fp, capabilities=caps)
                            self.browser.switch_to_window(self.browser.window_handles[0])
                        else:
                            print('"wires" or "geckodriver" not found in path. Exiting.')
                            sys.exit(1)
        else:
            raise UserWarning('No valid driver detected.')

        # Raise window automatically
        if self.browser:
            self.focus_window()

    def stop(self):
        '''
        Stops Selenium. Also stops XVFB if it was launched as a part of this
        class run.

        Note:

            Anything you don't stop here will need to be cleaned up with a kill
            command if you launched it outside of nosetests.

        '''
        print("\nStopping the browser...")
        self.browser.quit()
        if self.xvfb:
            print("\nStopping the XVFB display...")
            self.display.stop()

    # Helper functions:
    def wait_for(self, method, **kwargs):
        '''
        Wait for the supplied method to return True. A simple wrapper for _wait_for().

        Parameters
        ----------
        method: callable
                The function that determines the conditions for the wait to finish
        timeout: int
                Number of seconds to wait for `method` to return True
        '''
        self._wait_for(method, **kwargs)

    def back(self):
        '''
        Goes one step back in the browser's history.
        Just a convenient wrapper around the browser's back command
        '''
        self.browser.back()

    def forward(self):
        '''
        Goes one step forward in the browser's history.
        Just a convenient wrapper around the browser's forward command
        '''
        self.browser.forward()

    def click(self, selector, elem=None):
        '''
        Clicks an element.

        Parameters
        ----------
        selector: str
            A CSS selector to search for. This can be any valid CSS selector..

        '''
        self.wait_for_presence(selector)

        self.scroll_to_element(selector)

        self.wait_for_clickable(selector)

        if not elem:
            elem = self.get_element(selector)

        elem.click()

    def get_js_errors(self):
        '''
        Uses the JSErrorCollector plugin for Chrome / Firefox to get any JS errors.

        [
            {
                'sourceName': u'tests/html/js_error.html',
                'pageUrl': u'tests/html/js_error.html',
                'errorMessage': 'ReferenceError: b is not defined',
                'lineNumber': 7
            }
        ]
        '''
        if self.driver in ('Chrome', 'Firefox'):
            return self.js('return window.JSErrorCollector_errors ? window.JSErrorCollector_errors.pump() : []')
        else:
            print("Checking for JS errors with this method only works in Firefox or Chrome")
            return []

    def _parse_item(self, tp):
        try:
            from faker import Faker
            fake = Faker()
        except ImportError:
            fake = None

        return_value = ''
        parts = tp.split('|')
        if parts[0] == 'eval':
            return_value = eval(str(parts[1]))
        elif parts[0] == 'vars':
            # Automatically default to 0 index if not passed.
            print(parts)
            if len(parts) == 2:
                parts.append('0')
            return self.yaml_vars[parts[1]][int(parts[2])]
        elif self.yaml_funcs.get(parts[0]):
            args_regex = '\[([^}]+)\]'  # Get list args: [1,2,3]
            if len(re.findall(args_regex, parts[1])):
                # If this is a list, let's just literal_eval this and use the values.
                args = literal_eval(parts[1])
                return_value = self.yaml_funcs[parts[0]](args)
            else:
                # Otherwise, these are positional arguments.
                pargs = [p.strip() for p in parts[1].split(',')]
                args = []
                for parg in pargs:
                    try:
                        # Try to convert ints to ints
                        arg = literal_eval(parg)
                    except ValueError:
                        # This is probably a string.
                        arg = parg
                    args.append(arg)

                return_value = self.yaml_funcs[parts[0]](*args)

        if fake and parts[0].startswith('fake'):
            base = parts[0].replace('fake_', '').replace('fake-', '')
            return_value = getattr(fake, base)()

        if parts[0] != 'vars' and not self.yaml_vars.get(parts[0]):
            self.yaml_vars[parts[0]] = []

        self.yaml_vars[parts[0]].append(return_value)

        return return_value

    def _import(self, to_import):
        try:
            parts = to_import.split('.')
            if len(parts) == 0:
                if not self.yaml_funcs.get(to_import):
                    self.yaml_funcs[to_import] = importlib.import_module(to_import)
            else:
                if not self.yaml_funcs.get(parts[-1]):
                    module = importlib.import_module(*parts)
                    self.yaml_funcs[parts[-1]] = getattr(module, parts[-1])
        except SystemError:
            print("Sorry, Python < 3.5 can't import {} via YAML.".format(to_import))

    def _run_command(self, command):
        '''
        Internal method for running a command from a parsed YAML script.

        Parameters
        ----------

        command: dict
            A dict where the key is a method of this class.

        '''
        pre_parse_regex = '\(\(([^}]+)\)\)'  # Grab things wrapped like so: (( something ))
        for k in command:
            if hasattr(self, k):
                if type(command[k]) is list:
                    # Loop over the arguments and pre-parse them.
                    for index, item in enumerate(command[k]):
                        if type(item) is not list:
                            if type(item) is not dict:
                                to_parse = [i.strip() for i in re.findall(pre_parse_regex, str(item))]
                                if to_parse:
                                    tp = self._parse_item(to_parse[0])
                                    command[k][index] = tp
                        else:
                            for subindex, subitem in enumerate(item):
                                to_parse = [si.strip() for si in re.findall(pre_parse_regex, subitem)]
                                if to_parse:
                                    tp = self._parse_item(to_parse[0])
                                    command[k][index][subindex] = tp

                    if type(command[k][0]) is list:
                        getattr(self, k)(command[k])
                    else:
                        getattr(self, k)(*command[k])
                else:
                    getattr(self, k)(command[k])
            else:
                if k == 'import':
                    self._import(command[k])
                elif k in ('value_of', 'text_of'):
                    if not self.yaml_vars.get(k):
                        self.yaml_vars[k] = []
                    if k == 'value_of':
                        value = self.get_value(command[k])
                    elif k == 'text_of':
                        value = self.get_text(command[k])
                    self.yaml_vars[k].append(value)

    def _load_yaml_file(self, filepath):
        from yaml import load
        from json import loads
        with open(filepath, 'r') as f:
            if filepath.lower().endswith('yaml') or filepath.lower().endswith('yml'):
                script = load(f)
            elif filepath.lower().endswith('json'):
                script = loads(f.read())
            else:
                print("Couldn't detect filetype from extension. Defaulting to YAML.")
                script = load(f)
        return script

    def command_script(self, filepath=None, script=None, errors=True, verbose=False):
        '''
        Runs a script of PyWebRunner command_script

        Parameters
        ----------
        script: list of dicts
            A list of dicts where the key is the method to execute.
        errors: bool
            Whether or not to call bail_out on error
        verbose:
            Print extra debugging information

        '''
        self._import('random.randint')
        self._import('random.choice')
        if not script and filepath:
            script = self._load_yaml_file(filepath)

        for index, command in enumerate(script):
            if type(command) is str:
                if hasattr(self, command):
                    getattr(self, command)()
            else:
                key = list(command.keys())[0]
                digits = len(str(len(script)))
                if verbose:
                    print('({}) Parsing: {}: {}'.format(str(index + 1).zfill(digits), key, command[key]))

                # If the include command is given, parse those commands in-place before
                # continuing. This allows yaml scripts to include and use other yaml files.
                if key == 'include':
                    i_script = self._load_yaml_file(command[key])
                    for i_index, i_command in enumerate(i_script):
                        if errors:
                            self._run_command(i_command)
                        else:
                            try:
                                self._run_command(i_command)
                            except Exception as e:
                                self.bail_out(exception=e, caller='command_script')
                                raise

                else:
                    if errors:
                        self._run_command(command)
                    else:
                        try:
                            self._run_command(command)
                        except Exception as e:
                            self.bail_out(exception=e, caller='command_script')
                            raise

    def get_log(self, log=None):
        '''
        Gets the console log for the browser.
        '''
        if not log:
            log = 'browser'
        log_list = self.browser.get_log(log)
        return log_list

    def set_timeout(self, timeout=90):
        '''
        Sets the global wait timeout.

        Parameters
        ----------
        timeout: int
            Amount of time to wait (in seconds) before accepting that an action cannot occur. (Crash)

        '''
        self.timeout = int(timeout)

    def focus_window(self, windex=None):
        '''
        Focuses on the window with index (#).

        Parameters
        ----------
        windex: int
            The index of the window to focus on. Defaults to the first window opened.

        '''
        if not windex:
            windex = 0
        self.browser.switch_to_window(self.browser.window_handles[windex])

    def focus_browser(self):
        '''
        Raises and closes an empty alert in order to focus the browser app in most OSes.
        '''
        self.js('alert("");')
        self.close_alert()

    def get_log_text(self):
        '''
        Gets the console log text for the browser.
        [{u'level': u'SEVERE',
        u'message': u'ReferenceError: foo is not defined',
        u'timestamp': 1450769357488,
        u'type': u''},
        {u'level': u'INFO',
        u'message': u'The character encoding of the HTML document was not declared. The document will render with garbled text in some browser configurations if the document contains characters from outside the US-ASCII range. The character encoding of the page must be declared in the document or in the transfer protocol.',
        u'timestamp': 1450769357498,
        u'type': u''}]
        '''
        log = self.get_log()
        log_text = ''
        log_items = [item['message'] for item in log]
        for item in log_items:
            log_text += item + '\n'
        return log_text

    def bail_out(self, exception=None, caller=None):
        '''
        Method for reporting and, optionally, bypassing errors during a command.

        Parameters
        ----------
        exception: Exception
            The exception object.
        caller: str
            The method that called the bail_out.

        '''
        print(caller)
        print(exception)
        self.stop()

    def click_all(self, selector):
        '''
        Clicks all elements.

        Parameters
        ----------
        selector: str
            A CSS selector to search for. This can be any valid CSS selector..
            All matching elements will be clicked.

        '''

        elements = self.get_elements(selector)
        for element in elements:
            if element.is_displayed:
                element.click()

    def get_page_source(self):
        '''
        Gets the source code of the page.
        '''
        src = self.browser.page_source
        return src

    def is_text_on_page(self, text):
        '''
        Finds text if it is present on the page.

        Parameters
        ----------
        text: str
            The text to search for.

        '''
        src = self.get_page_source()
        src = src.encode('ascii', errors='ignore')
        return bool(text in src)

    def scroll_browser(self, amount, direction='down'):
        '''
        Scrolls the browser by the given amount in the specified direction.

        Parameters
        ----------
        amount: int
            number of pixels to scroll

        direction: str
            (up, down, left, right) defaults to 'down'
        '''
        if direction in ('up', 'right'):
            amount = amount * -1

        if direction in ('up', 'down'):
            scroll_string = "window.scrollBy(0, {});".format(amount)

        if direction in ('right', 'left'):
            scroll_string = "window.scrollBy({}, 0);".format(amount)

        self.js(scroll_string)

    def scroll_to_element(self, selector, elem=None):
        '''
        Scrolls the given element into view.

        Parameters
        ----------
        selector: str
            Any valid css selector
        '''
        if not elem:
            elem = self.get_element(selector)

        # Before we do any scrolling, make sure BC isn't scrolling
        self.wait_for_invisible('.js-scrolling')

        self.js("arguments[0].scrollIntoView();", elem)

        # Find out if we're right on the edge of the screen
        w_size = self.browser.get_window_size()
        scrolled_location = elem.location_once_scrolled_into_view
        edge_threshold = 50
        bottom_diff = abs(w_size['height'] - scrolled_location['y'])

        scroll_direction = None
        if bottom_diff < edge_threshold:
            scroll_direction = ''
        elif scrolled_location['y'] < edge_threshold:
            scroll_direction = '-'

        if scroll_direction is not None:
            scroll_width = w_size['width'] / 2
            scroll_height = w_size['height'] / 2
            self.js("window.scrollBy({0}{1}, {0}{2});".format(scroll_direction,
                                                              scroll_width,
                                                              scroll_height))

        self.wait_for_visible(selector)

    def set_select_by_text(self, select, text):
        '''
        Set the selected value of a select element by the visible text.

        Parameters
        ----------
        select: str or selenium.webdriver.remote.webelement.WebElement
            Any valid CSS selector or a selenium element
        text: str
            The visible text in the select element option. (Not the value)

        '''
        if isinstance(select, str):
            elem = self.get_element(select)
        else:
            elem = select

        sel = Select(elem)
        sel.select_by_visible_text(text)

    def set_select_by_value(self, select, value):
        '''
        Set the selected value of a select element by the value.

        Parameters
        ----------
        select: str or selenium.webdriver.remote.webelement.WebElement
            Any valid CSS selector or a selenium element
        value: str
            The value on the select element option. (Not the visible text)

        '''
        if isinstance(select, str):
            elem = self.get_element(select)
        else:
            elem = select

        sel = Select(elem)
        sel.select_by_value(value)

    def move_to(self, selector, click=False):
        '''
        Move to the element matched by selector or passed as argument.

        Parameters
        ----------
        selector: str
            Any valid CSS selector
        click: bool
            Whether or not to click the element after hovering
            defaults to False
        '''
        try:
            elem = self.get_element(selector)

            action = webdriver.ActionChains(self.browser)
            action.move_to_element(elem)
            if click:
                action.click(elem)

            action.perform()
        except WebDriverException:
            print("move_to isn't supported with this browser driver.")


    def hover(self, selector, click=False):
        '''
        Hover over the element matched by selector and optionally click it.

        Parameters
        ----------
        selector: str
            Any valid CSS selector
        click: bool
            Whether or not to click the element after hovering
            defaults to False
        '''
        try:
            self.move_to(selector, click)
        except WebDriverException:
            print("hover isn't supported with this browser driver.")

    def get_elements(self, selector):
        '''
        Gets elements by CSS selector.

        Parameters
        ----------
        selector: str
            A CSS selector to search for. This can be any valid CSS selector.

        Returns
        -------
        list of selenium.webdriver.remote.webelement.WebElement
            A list of selenium element objects.

        '''
        elems = self.find_elements(selector)
        return elems

    def get_element(self, selector):
        '''
        Gets element by CSS selector.

        Parameters
        ----------
        selector: str
            A CSS/XPATH selector to search for. This can be any valid CSS/XPATH selector.

        Returns
        -------
        selenium.webdriver.remote.webelement.WebElement
            A selenium element object.

        '''
        elem = self.find_element(selector)
        return elem

    def get_text(self, selector):
        '''
        Gets text from inside of an element by CSS selector.

        Parameters
        ----------
        selector: str
            A CSS selector to search for. This can be any valid CSS selector.

        Returns
        -------
        str
            The text from inside of a selenium element object.

        '''
        elem = self.get_element(selector)
        return str(elem.text)

    def get_texts(self, selector):
        '''
        Gets all the text from all elements found by CSS selector.

        Parameters
        ----------
        selector: str
            A CSS selector to search for. This can be any valid CSS selector.

        Returns
        -------
        list of str
            A list of text strings from inside of all found selenium element objects.

        '''
        elems = self.get_elements(selector)
        texts = [str(e.text) for e in elems]
        return texts

    def get_value(self, selector):
        '''
        Gets value of an element by CSS selector.

        Parameters
        ----------
        selector: str
            A CSS selector to search for. This can be any valid CSS selector.

        Returns
        -------
        str
            The value of a selenium element object.

        '''
        elem = self.get_element(selector)
        if self.driver == 'Gecko':
            # Let's do this the stupid way because Mozilla thinks geckodriver is
            # so incredibly amazing.
            tag_name = elem.tag_name
            if tag_name == 'select':
                select = Select(elem)
                return select.all_selected_options[0].get_attribute('value')
            else:
                return elem.get_attribute('value')
        else:
            return elem.get_attribute('value')

    def send_key(self, selector, key, wait_for='presence', **kwargs):
        '''
        Sets value of an element by CSS selector.

        Parameters
        ----------
        selector: str
            A CSS selector to search for. This can be any valid CSS selector.

        key: str
            A str representation of a special key to send.

            Some available keys and their string representations:
            ::
                'ADD' = u'\ue025'
                'ALT' = u'\ue00a'
                'ARROW_DOWN' = u'\ue015'
                'ARROW_LEFT' = u'\ue012'
                'ARROW_RIGHT' = u'\ue014'
                'ARROW_UP' = u'\ue013'
                'BACKSPACE' = u'\ue003'
                'BACK_SPACE' = u'\ue003'
                'CANCEL' = u'\ue001'
                'CLEAR' = u'\ue005'
                'COMMAND' = u'\ue03d'
                'CONTROL' = u'\ue009'
                'DECIMAL' = u'\ue028'
                'DELETE' = u'\ue017'
                'DIVIDE' = u'\ue029'
                'DOWN' = u'\ue015'
                'END' = u'\ue010'
                'ENTER' = u'\ue007'
                'EQUALS' = u'\ue019'
                'ESCAPE' = u'\ue00c'
                'F1' = u'\ue031'
                'F10' = u'\ue03a'
                'F11' = u'\ue03b'
                'F12' = u'\ue03c'
                'F2' = u'\ue032'
                'F3' = u'\ue033'
                'F4' = u'\ue034'
                'F5' = u'\ue035'
                'F6' = u'\ue036'
                'F7' = u'\ue037'
                'F8' = u'\ue038'
                'F9' = u'\ue039'
                'HELP' = u'\ue002'
                'HOME' = u'\ue011'
                'INSERT' = u'\ue016'
                'LEFT' = u'\ue012'
                'LEFT_ALT' = u'\ue00a'
                'LEFT_CONTROL' = u'\ue009'
                'LEFT_SHIFT' = u'\ue008'
                'META' = u'\ue03d'
                'MULTIPLY' = u'\ue024'
                'NULL' = u'\ue000'
                'NUMPAD0' = u'\ue01a'
                'NUMPAD1' = u'\ue01b'
                'NUMPAD2' = u'\ue01c'
                'NUMPAD3' = u'\ue01d'
                'NUMPAD4' = u'\ue01e'
                'NUMPAD5' = u'\ue01f'
                'NUMPAD6' = u'\ue020'
                'NUMPAD7' = u'\ue021'
                'NUMPAD8' = u'\ue022'
                'NUMPAD9' = u'\ue023'
                'PAGE_DOWN' = u'\ue00f'
                'PAGE_UP' = u'\ue00e'
                'PAUSE' = u'\ue00b'
                'RETURN' = u'\ue006'
                'RIGHT' = u'\ue014'
                'SEMICOLON' = u'\ue018'
                'SEPARATOR' = u'\ue026'
                'SHIFT' = u'\ue008'
                'SPACE' = u'\ue00d'
                'SUBTRACT' = u'\ue027'
                'TAB' = u'\ue004'
                'UP' = u'\ue013'

        kwargs:
            passed on to wait_for_*
        '''
        self._wait_for_presence_or_visible(selector, wait_for, **kwargs)

        elem = self.get_element(selector)

        if hasattr(Keys, key.upper()):
            elem.send_keys(getattr(Keys, key.upper()))

    def drag_and_drop(self, from_selector, to_selector):
        '''
        Drags an element into another.

        Parameters
        ----------
        from_selector: str
            A CSS selector to search for. This can be any valid CSS selector.
            Element to be dragged.

        to_selector: str
            A CSS selector to search for. This can be any valid CSS selector.
            Target element to be dragged into.

        '''

        from_element = self.get_element(from_selector)
        to_element = self.get_element(to_selector)
        ActionChains(self.browser).drag_and_drop(from_element, to_element).perform()

    def set_values(self, values, clear=True, blur=True, **kwargs):
        '''
        Sets values of elements by CSS selectors.

        Parameters
        ----------
        values: list of list or dict or list of dict
            A list of lists where index 0 is a selector string and 1 is a value.

        clear: bool
            Whether or not we should clear the element's value first.
            If false, value will be appended to the current value of the element.

        blur: bool
            Whether or not we should blur the element after setting the value.
            Defaults to True

        kwargs:
            passed on to wait_for_visible

        '''
        if isinstance(values, dict):
            # If the entire var is a dict, just use all the key/value pairs
            for key in values:
                self.set_value(key, values[key], clear=clear, blur=blur, **kwargs)
        else:
            # If not a dict it's a list/tuple of things (dicts or lists / tuples)
            for row in values:
                if isinstance(row, dict):
                    # If it is a dict use it's key / value pairs.
                    for key in row:
                        self.set_value(key, row[key], clear=clear, blur=blur, **kwargs)
                else:
                    # Otherwise just use the list / tuple positions
                    self.set_value(row[0], row[1], clear=clear, blur=blur, **kwargs)

    def wait(self, seconds=500):
        '''
        Sleeps for some amount of time.

        Parameters
        ----------

        seconds: int
            Seconds to sleep for.

        '''
        # You probably shouldn't use this for anything
        # real in tests. I use this for pausing execution.
        sleep(seconds)

    def set_value(self, selector, value, clear=True, blur=True, **kwargs):
        '''
        Sets value of an element by CSS selector.

        Parameters
        ----------
        selector: str
            A CSS selector to search for. This can be any valid CSS selector.

        value: str
            The value to set on the element matched by the selector.

        clear: bool
            Whether or not we should clear the element's value first.
            If false, value will be appended to the current value of the element.

        blur: bool
            Whether or not we should blur the element after setting the value.
            Defaults to True

        kwargs:
            passed on to wait_for_visible

        '''
        typing = kwargs.get('typing', False)
        typing_speed = kwargs.get('typing_speed', 3)
        typing_max_delay = kwargs.get('typing_max_delay', .33)
        self.wait_for_visible(selector, **kwargs)

        elem = kwargs.get('elem')
        if not elem:
            elem = self.get_element(selector)

        if elem.tag_name == 'select':
            self.set_select_by_value(elem, value)
        else:
            if clear:
                self.clear(selector)
            if typing:
                for k in value:
                    delay = random() / typing_speed
                    if delay > typing_max_delay:
                        delay = typing_max_delay
                    sleep(delay)
                    elem.send_keys(k)
            else:
                elem.send_keys(value)

            if self.driver == 'Gecko':
                # Thank you so much Mozilla. This is awesome to have to do.
                self.js("arguments[0].setAttribute('value', '" + value +"')", elem)

        if blur:
            elem.send_keys(Keys.TAB)

    def set_selectize(self, selector, value, text=None, clear=True, blur=False):
        '''
        Sets visible value of a selectize control based on the "selectized" element.

        Parameters
        ----------
        selector: str
            A CSS selector to search for. This can be any valid CSS selector.

        value: str
            The value of the option to select.
            (Stored Value)

        text: str
            The visible value that the user sees.
            (Visible value, if different than the stored value)

        clear: bool
            Whether or not we should clear the selectize value first.
            Defaults to True

        blur: bool
            Whether or not we should blur the element after setting the value.
            This corresponds to the 'selectOnTab' selecize setting.
            Defaults to False
        '''
        selectize_control = selector + ' + .selectize-control'
        selectize_input = selectize_control + ' input'

        # Make sure the selectize control is active so the input is visible
        self.click(selectize_control)

        input_element = self.get_element(selectize_input)

        if clear:
            input_element.send_keys(Keys.BACK_SPACE)

        input_element.send_keys(text or value)

        # Wait for options to be rendered
        self.wait_for_visible(selectize_control + ' .has-options')

        if blur:
            input_element.send_keys(Keys.TAB)
        else:
            # Click the option for the given value
            self.click(selectize_control + ' .option[data-value="{}"]'.format(value))

    def clear(self, selector):
        '''
        Clears value of an element by CSS selector.

        Parameters
        ----------
        selector: str
            A CSS selector to search for. This can be any valid CSS selector.

        '''
        elem = self.get_element(selector)
        if elem:
            elem.clear()

    def current_url(self):
        '''
        Gets current URL of the browser object.

        Returns
        -------
        str
            The curent URL.

        '''
        return self.browser.current_url

    def go(self, address):
        '''
        Go to a web address. (self.browser should be available, but not needed.)

        Parameters
        ----------
        address: str
            The address (URL)

        '''
        self.browser.get(address)

    def count(self, selector):
        '''
        Counts the number of elements that match CSS/XPATH selector.

        Parameters
        ----------
        selector: str
            A CSS/XPATH selector to search for. This can be any valid CSS/XPATH selector.

        Returns
        -------
        int: Number of matching elements.

        '''
        return len(self.get_elements(selector))

    def find_element(self, selector):
        '''
        Finds an element by CSS/XPATH selector.

        Parameters
        ----------
        selector: str
            A CSS/XPATH selector to search for. This can be any valid CSS/XPATH selector.

        Returns
        -------
        selenium.webdriver.remote.webelement.WebElement or None
            Returns an element or nothing at all

        '''
        elem = None
        try:
            if selector.startswith('/'):
                elem = self.browser.find_element_by_xpath(selector)
            else:
                elem = self.browser.find_element_by_css_selector(selector)
        except NoSuchElementException:
            pass

        return elem

    def find_elements(self, selector):
        '''
        Finds elements by CSS/XPATH selector.

        Parameters
        ----------
        selector: str
            A CSS/XPATH selector to search for. This can be any valid CSS/XPATH selector.

        Returns
        -------
        list of selenium.webdriver.remote.webelement.WebElement or list
            Returns a list of elements or empty list

        '''
        elems = []
        try:
            if selector.startswith('/'):
                elems = self.browser.find_elements_by_xpath(selector)
            else:
                elems = self.browser.find_elements_by_css_selector(selector)
        except NoSuchElementException:
            pass

        return elems

    def refresh_page(self, refresh_method="url"):
        '''
        Refreshes the current page

        Parameters
        ----------
        method: str
            The method used to refresh the page.
            Defaults to "url" which navigates to the current_url

        '''
        if refresh_method == "url":
            self.browser.get(self.browser.current_url)
        elif refresh_method == "js":
            self.js('window.location.reload(true);')

    def js(self, js_str, *args):
        '''
        Run some JavaScript and return the result.

        Parameters
        ----------
        js_str: str
            A string containing some valid JavaScript to be ran on the page.

        Returns
        -------
        str or bool or list or dict
            Returns the result of the JS evaluation.

        '''
        return self.browser.execute_script(js_str, *args)

    def _find_elements(self, row):
        '''
        Find elements using a name, css selector, class, xpath, or id.

        Parameters
        ----------
        row: dict
            A dict where the key is the search method
            and the value is what is passed to Selenium

        Returns
        -------
        list of selenium.webdriver.remote.webelement.WebElement
            A list of selenium element objects.

        '''
        elems = []
        try:
            if 'name' in row:
                elems = self.browser.find_elements_by_name(row['name'])
            elif 'css' in row:
                elems = self.browser.find_elements_by_css_selector(row['css'])
            elif 'class' in row:
                elems = self.browser.find_elements_by_class_name(row['class'])
            elif 'xpath' in row:
                elems = self.browser.find_elements_by_xpath(row['xpath'])
            else:
                elems = self.browser.find_elements_by_id(row['id'])
        except NoSuchElementException:
            pass
        finally:
            return elems

    def save_page_source(self, path='/tmp/selenium-page-source.html'):
        '''
        Saves the raw page html in it's current state. Takes a path as a parameter.

        Parameters
        ----------
        path: str
            Defaults to: /tmp/selenium-page-source.html

        '''
        page_source = self.browser.page_source

        out_file = open(path, 'w')
        out_file.write(page_source.encode('utf8'))
        out_file.close()

    def screenshot(self, path=None):
        '''
        Saves a screenshot. Takes a path as a parameter.

        Parameters
        ----------
        path: str
            Defaults to: /tmp/selenium-screenshot.png

        '''
        if not path:
            path = '/tmp/selenium-screenshot.png'

        # if isinstance(self.browser, webdriver.remote.webdriver.WebDriver):
        #     # Get base64 screenshot from the remote.
        #     base64_data = self.browser.get_screenshot_as_base64()
        #     ss_data = base64.decodestring(base64_data)
        #     with open(path, 'w') as f:
        #         f.write(ss_data)
        #         f.close()
        # else:
        self.browser.save_screenshot(path)

    def fill(self, form_dict):
        '''
        Fills a form using Selenium. This helper will save a lot of time
        and effort because working with form data can be tricky and gross.

        Parameters
        ----------
        form_dict: dict
            Takes in a dict where the keys are CSS selectors
            and the values are what will be applied to them.

        '''
        form_list = []
        for key in form_dict:
            form_list.append({'css': key, 'value': form_dict[key]})
        self.fill_form(form_list)

    def fill_form(self, form_list):
        '''
        This helper can be used directly but it is much easier
        to use the "fill" method instead.

        Parameters
        ----------
        form_list: list of dict
            A list of dictionaries where the key is the search method
            and the value is what is passed to Selenium
        clear: bool
            True/False value indicating whether or not to clear out
            the input currently in any text inputs.

        '''
        for row in form_list:
            elems = self._find_elements(row)
            # If the length is greater than 1, it should be a checkbox or radio.
            if len(elems) > 1:
                # Get the element type we are dealing with.
                tag_name = elems[0].tag_name
                tag_type = elems[0].get_attribute('type')

                if tag_type == 'radio':
                    for elem in elems:
                        tag_value = elem.get_attribute('value')
                        if tag_value == row['value']:
                            # Select the right radio button
                            elem.click()

                elif tag_type == 'checkbox':
                    # We need to handle checkboxes differently than radio buttons.
                    # (More than one can be checked so we must handle that.)
                    for elem in elems:
                        tag_value = elem.get_attribute('value')
                        if not isinstance(row['value'], list):
                            # Put single items in a list so we can loop.
                            row['value'] = [row['value']]

                        for value in row['value']:
                            # Loop over all the values and check the ones we want.
                            # Un-check the ones we don't want.
                            if tag_value == value:
                                if not elem.is_selected():
                                    elem.click()
                            else:
                                if elem.is_selected():
                                    if tag_value not in row['value']:
                                        elem.click()

            elif len(elems) == 1:
                # Handle every other form element type since they are much
                # more straightforward.
                elem = elems[0]
                tag_name = elem.tag_name

                if tag_name in ('input', 'textarea'):
                    # File upload needs a path to a file.
                    self.set_value('', row['value'], elem=elem)

                elif tag_name == 'select':
                    self.set_value('', row['value'], elem=elem)

            else:
                print("{} Element not found.".format(row))

    # Custom asynchronous wait helpers
    def _wait_for(self, wait_function, **kwargs):
        '''
        Wrapper to handle the boilerplate involved with a custom wait.

        Parameters
        ----------
        wait_function: func
            This can be a builtin selenium wait_for class,
            a special wait_for class that implements the __call__ method,
            or a lambda function
        timeout: int
            The number of seconds to wait for the given condition
            before throwing an error.
            Overrides WebRunner.timeout

        '''
        try:
            wait = WebDriverWait(self.browser, kwargs.get('timeout') or self.timeout)
            wait.until(wait_function)
        except TimeoutException:
          if self.driver == 'Gecko':
              print("Geckodriver can't use the text_to_be_present_in_element_value wait for some reason.")
          else:
              raise

    def wait_for_alert(self, **kwargs):
        '''
        Shortcut for waiting for alert. If it not ends with exception, it
        returns that alert.
        '''
        self._wait_for(self.alert_present, **kwargs)

    def wait_for_presence(self, selector='', **kwargs):
        '''
        Wait for an element to be present. (Does not need to be visible.)

        Parameters
        ----------
        selector: str
            A CSS selector to search for. This can be any valid CSS selector.

        kwargs:
            Passed on to _wait_for

        '''
        if selector.startswith('/'):
            by = By.XPATH
        else:
            by = By.CSS_SELECTOR
        self._wait_for(EC.presence_of_element_located((by, selector)) or
                       EC.presence_of_elements_located((by, selector)),
                       **kwargs)

    def wait_for_clickable(self, selector='', **kwargs):
        '''
        Wait for an element to be clickable.

        Parameters
        ----------
        selector: str
            A CSS selector to search for. This can be any valid CSS selector.

        kwargs:
            Passed on to _wait_for

        '''
        if selector.startswith('/'):
            by = By.XPATH
        else:
            by = By.CSS_SELECTOR
        self._wait_for(EC.element_to_be_clickable((by, selector)), **kwargs)

    def wait_for_ko(self, selector='', **kwargs):
        '''
        Wait for an element to be bound by Knockout JS.

        Parameters
        ----------
        selector: str
            A CSS selector to search for. This can be any valid CSS selector.
        kwargs:
            Passed on to _wait_for
        '''
        self.wait_for_presence(selector)

        ieo_func = 'function __isEmptyObject(obj){var name;for(name in obj){return false;}return true;}'
        js_check_bound = "{0}return !__isEmptyObject(ko.dataFor(document.querySelectorAll('{1}')[0]));"
        self.wait_for_js(js_check_bound.format(ieo_func, selector), **kwargs)

    def wait_for_url(self, url='', **kwargs):
        '''
        Wait for the current url to match the given url.

        Parameters
        ----------
        url: str
            A regular expression to match against the current url
        kwargs:
            Passed on to _wait_for

        '''
        self._wait_for(expect_url_match(url), **kwargs)

    def wait_for_visible(self, selector='', **kwargs):
        '''
        Wait for an element to be visible.

        Parameters
        ----------
        selector: str
            A CSS selector to search for. This can be any valid CSS selector.

        kwargs:
            Passed on to _wait_for

        '''
        if selector.startswith('/'):
            by = By.XPATH
        else:
            by = By.CSS_SELECTOR
        self._wait_for(EC.visibility_of_element_located((by, selector)),
                       **kwargs)

    def _wait_for_presence_or_visible(self, selector, wait_for, **kwargs):
        '''
        Wrapper around wait_for_presence and wait_for_visible that takes a
        string to decide which one to use.
        '''
        if wait_for == 'presence':
            self.wait_for_presence(selector, **kwargs)
        elif wait_for == 'visible':
            self.wait_for_visible(selector, **kwargs)

    def wait_for_invisible(self, selector='', **kwargs):
        '''
        Wait for an element to be invisible.

        Parameters
        ----------
        selector: str
            A CSS selector to search for. This can be any valid CSS selector.

        kwargs:
            Passed on to _wait_for

        '''
        if selector.startswith('/'):
            by = By.XPATH
        else:
            by = By.CSS_SELECTOR
        self._wait_for(EC.invisibility_of_element_located((by, selector)),
                       **kwargs)

    def wait_for_all_invisible(self, selector='', **kwargs):
        '''
        Wait for all elements that match selector to be invisible.

        Parameters
        ----------
        selector: str
            A CSS selector to search for. This can be any valid CSS selector.

        kwargs:
            Passed on to _wait_for

        '''
        all_matches = self.get_elements(selector)

        for match in all_matches:
            self._wait_for(invisibility_of(match), **kwargs)

    def wait_for_js(self, js_script, **kwargs):
        '''
        Wait for the given JS to return true.

        Parameters
        ----------
        js_script: str
            valid JS that will run in the page dom

        kwargs:
            passed on to _wait_for

        '''
        self._wait_for(lambda browser: bool(browser.execute_script(js_script)),
                       **kwargs)

    def wait_for_text(self, selector='', text='', **kwargs):
        '''
        Wait for an element to contain a specific string.

        Parameters
        ----------
        selector: str
            A CSS selector to search for. This can be any valid CSS selector.

        text: str
            The string to look for. This must be precise.
            (Case, punctuation, UTF characters... etc.)
        kwargs:
            Passed on to _wait_for

        '''
        if selector.startswith('/'):
            by = By.XPATH
        else:
            by = By.CSS_SELECTOR
        self._wait_for(EC.text_to_be_present_in_element((by, selector),
                                                        text), **kwargs)

    def wait_for_text_in_value(self, selector='', text='', **kwargs):
        '''
        Wait for an element's value to contain a specific string.

        Parameters
        ----------
        selector: str
            A CSS selector to search for. This can be any valid CSS selector.

        text: str
            The string to look for. This must be precise.
            (Case, punctuation, UTF characters... etc.)
        kwargs:
            Passed on to _wait_for

        '''
        if selector.startswith('/'):
            by = By.XPATH
        else:
            by = By.CSS_SELECTOR
        self._wait_for(EC.text_to_be_present_in_element_value((by, selector),
                                                              text), **kwargs)

    def wait_for_selected(self, selector='', selected=True, **kwargs):
        '''
        Wait for an element (checkbox/radio) to be selected.

        Parameters
        ----------
        selector: str
            A CSS selector to search for. This can be any valid CSS selector.

        selected: bool
            Whether or not the element should be selected. Default True

        kwargs:
            Passed on to _wait_for

        '''
        if selector.startswith('/'):
            by = By.XPATH
        else:
            by = By.CSS_SELECTOR
        self._wait_for(EC.element_located_selection_state_to_be((by, selector),
                                                                selected), **kwargs)

    def wait_for_title(self, title, **kwargs):
        '''
        Wait for the page title to match given title.

        Parameters
        ----------
        title: str
            The page title to wait for

        kwargs:
            Passed on to _wait_for

        '''
        self._wait_for(EC.title_is(title), **kwargs)

    def wait_for_value(self, selector='', value='', **kwargs):
        '''
        Wait for an element to contain a specific string.

        Parameters
        ----------
        selector: str
            A CSS selector to search for. This can be any valid CSS selector.

        value: str
            The string to look for. This must be precise.
            (Case, punctuation, UTF characters... etc.)
        kwargs:
            Passed on to _wait_for

        '''
        if selector.startswith('/'):
            by = By.XPATH
        else:
            by = By.CSS_SELECTOR
        self._wait_for(EC.text_to_be_present_in_element_value((by, selector),
                                                              value), **kwargs)

    def wait_for_opacity(self, selector, opacity, **kwargs):
        '''
        Wait for an element to reach a specific opacity.

        Parameters
        ----------
        selector: str
            A CSS selector to search for. This can be any valid CSS selector.

        opacity: float
            The opacity to wait for.

        kwargs:
            Passed on to _wait_for

        '''

        def _wait_for_opacity(self, browser):
            return str(self.get_element(selector).value_of_css_property('opacity')) == str(opacity)

        self._wait_for(partial(_wait_for_opacity, self), **kwargs)

    def switch_to_window(self, window_name=None, title=None, url=None):
        '''
        Switch to window by name, title, or url.

        Parameters
        ----------
        window_name: str
            The name of the window to switch to.

        title: str
            The title of the window you wish to switch to.

        url: str
            URL of the window you want to switch to.

        '''
        if window_name:
            self.browser.switch_to_window(window_name)
            return

        else:
            for window_handle in self.browser.window_handles:
                self.browser.switch_to_window(window_handle)

                if title and self.browser.title == title:
                    return

                if url and self.browser.current_url == url:
                    return

        raise NoSuchWindowException('Window not found: {}, {}, {}'.format(window_name, title, url))

    def close_window(self, window_name=None, title=None, url=None):
        """
        Close window by name, title, or url.

        Parameters
        ----------
        window_name: str
            The name of the window to switch to.

        title: str
            The title of the window you wish to switch to.

        url: str
            URL of the window you want to switch to.

        """
        main_window_handle = self.browser.current_window_handle
        self.switch_to_window(window_name, title, url)
        self.browser.close()
        self.switch_to_window(main_window_handle)

    def close_all_other_windows(self):
        '''
        Closes all windows except for the currently active one.
        '''
        main_window_handle = self.browser.current_window_handle
        for window_handle in self.browser.window_handles:
            if window_handle == main_window_handle:
                continue

            self.switch_to_window(window_handle)
            self.browser.close()

        self.switch_to_window(main_window_handle)

    def close_alert(self, ignore_exception=False):
        '''
        Closes any alert that is present. Raises an exception if no alert is found.

        Parameters
        ----------

        ignore_exception: bool
            Does not throw an exception if an alert is not present.

        '''
        try:
            alert = self.get_alert()
            alert.accept()
        except NoAlertPresentException:
            if not ignore_exception:
                raise

    def get_alert(self):
        '''
        Returns instance of :py:obj:`~selenium.webdriver.common.alert.Alert`.
        '''
        return Alert(self.browser)

    def alert_present(self):
        '''
        Checks to see if an alert is present.
        '''
        alert = Alert(self.browser)
        try:
            alert.text
            return True

        except NoAlertPresentException:
            return False


class expect_url_match(object):
    '''Checks for the current url to match. '''

    def __init__(self, url_check):
        self.url_check = url_check

    def __call__(self, driver):
        return re.search(self.url_check, driver.current_url)


class invisibility_of(object):
    ''' Checks for a known element to be invisible.
        Much like the builtin visibility_of:
        https://github.com/SeleniumHQ/selenium/search?utf8=%E2%9C%93&q=visibility_of
    '''

    def __init__(self, element):
        self.element = element

    def __call__(self, driver):
        try:
            return (not self.element.is_displayed())
        except EC.StaleElementReferenceException:
            # If the element reference is no longer valid,
            # it was likely removed from the dom and is no longer visible
            return True
