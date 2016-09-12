import unittest
from appium import webdriver
from selenium import webdriver as seleniumWebdriver
from sauceclient import SauceClient
import sys
from hotdog import Mustard
from hotdog.Results import UploadResults
from hotdog.Config import GetConfig
from time import sleep, time
from appium_selector.DeviceSelector import DeviceSelector
import builtins
import threading
import webium.settings
from hotdog.BaseDriver import BaseWebDriver
webium.settings.implicit_timeout = 5

class HotDogBaseTest(unittest.TestCase):

    DefaultWebDriver = BaseWebDriver

    #Boilerplate Settings Do not Change
    #Change in Config.xml
    SAUCE_USERNAME = GetConfig('SAUCE_USERNAME')
    SAUCE_ACCESS = GetConfig('SAUCE_ACCESS')

    SAUCE_URL = "http://%s:%s@ondemand.saucelabs.com:80/wd/hub" % (SAUCE_USERNAME, SAUCE_ACCESS)
    GRID_URL = GetConfig('GRID_URL') + '/wd/hub'
    LOCAL_APPIUM_URL = GetConfig('LOCAL_APPIUM_URL')
    # set SKIP_SELECTOR to bypass the device selector & run local with platfrom from LOCAL_BROWSER
    try:
        SKIP_SELECTOR = GetConfig('SKIP_SELECTOR')
        LOCAL_BROWSER = GetConfig('LOCAL_BROWSER')
    except:
        #xml file is missing SKIP_SELECTOR/LOCAL_BROWSER
        SKIP_SELECTOR = 'False'
        # LOCAL_BROWSER = 'firefox'   # will not be used

    failed = False
    skipMustard = False
    defaultTestResult = UploadResults

    timersStart = {}
    timersTotal = {}
    testcase_id = ''

    @classmethod
    def setUpClass(cls, platform='mobile'):
        if not hasattr(builtins, 'threadlocal'):
            runLocal = False
            builtins.threadlocal = threading.local()

            if HotDogBaseTest.SKIP_SELECTOR == 'True':
                # skip device selector, fill in defaults for running locally
                builtins.threadlocal.config = {
                    'desiredCaps': {'browserName':  'Local',
                                    'deviceName':   'Local',
                                    'platformName': 'Local',
                                    'version':      'Local'},
                    'options': {'manufacturer': 'local',
                                'mustard':       False,
                                'provider':     'local-'+HotDogBaseTest.LOCAL_BROWSER,
                                'osv':          'Local',
                                'model':        'local',
                                }
                }
            else:
                # use selector to get device/platform
                builtins.threadlocal.config = DeviceSelector(platform=platform).getDevice()[0]

            provider = builtins.threadlocal.config['options']['provider']
            if 'platformName' in builtins.threadlocal.config['desiredCaps']:
                if builtins.threadlocal.config['desiredCaps']['platformName'].upper() == 'ANDROID':
                    builtins.threadlocal.config['desiredCaps']['app'] = GetConfig('ANDROID_APP_URL')
                else:
                    builtins.threadlocal.config['desiredCaps']['app'] = GetConfig('IOS_APP_URL')
            desired_caps = builtins.threadlocal.config['desiredCaps']
            try:
                if 'grid' in provider:
                    url = GetConfig('GRID_URL') + '/wd/hub'
                elif 'sauce' in provider:
                    url = "http://%s:%s@ondemand.saucelabs.com:80/wd/hub" % (GetConfig('SAUCE_USERNAME'), GetConfig('SAUCE_ACCESS'))
                    if desired_caps['browserName'] == 'internet explorer':
                        desired_caps['requireWindowFocus'] = True
                elif provider.lower() == 'local-chrome':
                    runLocal = True
                    builtins.threadlocal.driver = seleniumWebdriver.Chrome()
                elif provider.lower() == 'local-firefox':
                    runLocal = True
                    builtins.threadlocal.driver = seleniumWebdriver.Firefox()
                elif provider.lower() == 'local-safari':
                    runLocal = True
                    builtins.threadlocal.driver = seleniumWebdriver.Safari()
                elif provider.lower() == 'local-ie':
                    runLocal = True
                    builtins.threadlocal.driver = seleniumWebdriver.Ie()
                elif provider.lower() == 'mcweb':
                    url = GetConfig('MC_URL') + '/wd/hub'
                elif provider.lower() == 'mcmobile':
                    url = GetConfig('MC_URL') + '/wd/hub'
                else:
                    url = GetConfig('GRID_URL') + '/wd/hub'

                if not runLocal:
                    builtins.threadlocal.driver = webdriver.Remote(
                        url,
                        desired_caps
                    )
            except:
                #print("Testcase [%s] COULD NOT START on device [%s]" % (self._testMethodName, self.options['deviceName']))
                print(sys.exc_info()[1])
                raise unittest.SkipTest('Could not launch driver')


    def setUp(self):
        runLocal = False
        self.desired_caps = builtins.threadlocal.config['desiredCaps']
        self.options = builtins.threadlocal.config['options']
        self.resultLink = None
        self.provider = self.options['provider']
        if not builtins.threadlocal.driver:

            try:
                if 'grid' in self.provider:
                    url = self.GRID_URL
                elif 'sauce' in self.provider:
                    url = self.SAUCE_URL
                    if self.desired_caps['browserName'] == 'internet explorer':
                        self.desired_caps['requireWindowFocus'] = True
                elif self.provider.lower() == 'local-chrome':
                    runLocal = True
                    self.driver = seleniumWebdriver.Chrome()
                elif self.provider.lower() == 'local-firefox':
                    runLocal = True
                    self.driver = seleniumWebdriver.Firefox()
                elif self.provider.lower() == 'local-safari':
                    runLocal = True
                    self.driver = seleniumWebdriver.Safari()
                elif self.provider.lower() == 'local-ie':
                    runLocal = True
                    self.driver = seleniumWebdriver.Ie()
                elif self.provider.lower() == 'mcweb':
                    url = GetConfig('MC_URL') + '/wd/hub'
                elif self.provider.lower() == 'mcmobile':
                    url = GetConfig('MC_URL') + '/wd/hub'
                else:
                    url = self.GRID_URL

                if not runLocal:
                    self.driver = webdriver.Remote(
                        url,
                        self.desired_caps
                    )
                self.continueWithDriver = False
            except:
                print("Testcase [%s] COULD NOT START on device [%s]" % (self._testMethodName, self.options['deviceName']))
                print(sys.exc_info()[1])
                raise unittest.SkipTest('Could not launch driver')
            self.driver.__class__ = self.DefaultWebDriver
            builtins.threadlocal.driver = self.driver
            self.options['deviceName'] = self.environmentName()
            print("Testcase [%s] started on device [%s]" % (self._testMethodName, self.options['deviceName']))
            sleep(1)
        else:
            self.driver = builtins.threadlocal.driver
            self.driver.__class__ = self.DefaultWebDriver
            self.options['deviceName'] = self.environmentName()
            print("Testcase [%s] started on device [%s]" % (self._testMethodName, self.options['deviceName']))
            self.continueWithDriver = True

    def environmentName(self):
        if 'deviceName' in self.options:
            return self.options['deviceName']
        elif 'udid' in self.desired_caps:
            return self.desired_caps['udid']
        else:
            return self.options['provider']

    def tearDown(self):
        if 'sauce' in self.provider.lower():
            sauce = SauceClient(self.SAUCE_USERNAME, self.SAUCE_ACCESS)
            self.resultLink = "https://saucelabs.com/beta/tests/%s" % self.driver.session_id
            try:
                if sys.exc_info() == (None, None, None):
                    sauce.jobs.update_job(self.driver.session_id, passed=True, name=self._testMethodName)
                else:
                    sauce.jobs.update_job(self.driver.session_id, passed=False, name=self._testMethodName)
            except:
                pass

    @classmethod
    def tearDownClass(cls):
        cls.RemoveApp()

    @classmethod
    def RemoveApp(self):
        if 'mobile' in builtins.threadlocal.config['options']['provider']:
            try: builtins.threadlocal.driver.close_app()
            except: pass
            try: builtins.threadlocal.driver.remove_app(GetConfig('IOS_BUNDLE_ID'))
            except: pass
            try: builtins.threadlocal.driver.remove_app(GetConfig('ANDROID_BUNDLE_ID'))
            except: pass
        try: builtins.threadlocal.driver.quit()
        except: pass

    def run(self, result=None):
        super().run( result= self.defaultTestResult())

    def timerStart(self, name):
        self.timersStart[name] = time()

    def timerStop(self, name):
        self.timersTotal[name] = time() - self.timersStart[name]
        if self.options['mustard']:
            Mustard.UploadPerformance(Mustard.getDeviceID(self), name, self.timersTotal[name])


