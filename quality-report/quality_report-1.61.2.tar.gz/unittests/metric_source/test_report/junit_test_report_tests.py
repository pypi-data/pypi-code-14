"""
Copyright 2012-2016 Ministerie van Sociale Zaken en Werkgelegenheid

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import datetime
import io
import unittest
import urllib2

from qualitylib.metric_source import JunitTestReport


class FakeUrlOpener(object):  # pylint: disable=too-few-public-methods
    """ Fake URL opener. """
    contents = u''

    def url_open(self, url):
        """ Return the html or raise an exception. """
        if 'raise' in url:
            raise urllib2.HTTPError(None, None, None, None, None)
        else:
            return io.StringIO(self.contents)


class JunitTestReportTest(unittest.TestCase):
    """ Unit tests for the Junit test report class. """
    def setUp(self):
        self.__opener = FakeUrlOpener()
        self.__junit = JunitTestReport(url_open=self.__opener.url_open)

    def test_test_report(self):
        """ Test retrieving a Junit test report. """
        self.__opener.contents = u'<testsuites>' \
                                 '  <testsuite tests="12" failures="2" errors="0" skipped="1" disabled="0">' \
                                 '    <testcase><failure/></testcase>' \
                                 '    <testcase><failure/></testcase>' \
                                 '  </testsuite>' \
                                 '</testsuites>'
        self.assertEqual(2, self.__junit.failed_tests('url'))
        self.assertEqual(9, self.__junit.passed_tests('url'))
        self.assertEqual(1, self.__junit.skipped_tests('url'))

    def test_multiple_test_suites(self):
        """ Test retrieving a Junit test report with multiple suites. """
        self.__opener.contents = u'<testsuites>' \
                                 '  <testsuite tests="5" failures="1" errors="0" skipped="1" disabled="1">' \
                                 '    <testcase><failure/><failure/></testcase>' \
                                 '  </testsuite>' \
                                 '  <testsuite tests="3" failures="1" errors="1" skipped="0" disabled="0">' \
                                 '    <testcase><failure/></testcase>' \
                                 '  </testsuite>' \
                                 '</testsuites>'
        self.assertEqual(3, self.__junit.failed_tests('url'))
        self.assertEqual(3, self.__junit.passed_tests('url'))
        self.assertEqual(2, self.__junit.skipped_tests('url'))

    def test_http_error(self):
        """ Test that the default is returned when a HTTP error occurs. """
        self.assertEqual(-1, self.__junit.failed_tests('raise'))
        self.assertEqual(-1, self.__junit.passed_tests('raise'))
        self.assertEqual(-1, self.__junit.skipped_tests('raise'))

    def test_incomplete_xml(self):
        """ Test that the default is returned when the xml is incomplete. """
        self.__opener.contents = u'<testsuites></testsuites>'
        self.assertEqual(-1, self.__junit.failed_tests('url'))

    def test_report_datetime(self):
        """ Test that the date and time of the test suite is returned. """
        self.__opener.contents = u'<testsuites>' \
                                 '  <testsuite name="Art" timestamp="2016-07-07T12:26:44">' \
                                 '  </testsuite>' \
                                 '</testsuites>'
        self.assertEqual(datetime.datetime(2016, 7, 7, 12, 26, 44), self.__junit.report_datetime('url'))

    def test_missing_report_datetime(self):
        """ Test that the minimum datetime is returned if the url can't be opened. """
        self.assertEqual(datetime.datetime.min, self.__junit.report_datetime('raise'))

    def test_incomplete_xml_datetime(self):
        """ Test that the minimum datetime is returned when the xml is incomplete. """
        self.__opener.contents = u'<testsuites></testsuites>'
        self.assertEqual(datetime.datetime.min, self.__junit.report_datetime('url'))

    def test_incomplete_xml_no_timestamp(self):
        """ Test that the minimum datetime is returned when the xml is incomplete. """
        self.__opener.contents = u'<testsuites><testsuite></testsuite></testsuites>'
        self.assertEqual(datetime.datetime.min, self.__junit.report_datetime('url'))

    def test_urls(self):
        """ Test that the urls point to the HTML versions of the reports. """
        self.assertEqual(['http://server/html/htmlReport.html'],
                         self.__junit.metric_source_urls('http://server/junit/junit.xml'))
