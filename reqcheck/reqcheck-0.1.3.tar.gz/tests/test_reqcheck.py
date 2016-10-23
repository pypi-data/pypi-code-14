from datetime import datetime, timedelta
import mock
import os
from pkg_resources import parse_version
from requests.exceptions import RequestException
import shutil
import six
import subprocess
import sys
import tempfile
import unittest

import reqcheck

class GetPkgInfoTest(unittest.TestCase):
    def setUp(self):
        self.get_patcher = mock.patch('requests.get')
        self.get_mock = self.get_patcher.start()
        
        self.response_mock = mock.Mock()
        self.get_mock.return_value = self.response_mock
    
    def tearDown(self):
        self.get_patcher.stop()
    
    def testMakesRequestToPypi(self):
        reqcheck.get_pkg_info('test_pkg')
        
        self.get_mock.assert_called_with('https://pypi.python.org/pypi/test_pkg/json')
    
    def testReturnsNoneWhenRequestRaisesException(self):
        self.get_mock.side_effect = RequestException()
        
        self.assertIsNone(reqcheck.get_pkg_info('test_pkg'))
    
    def testReturnsNoneWhenResponseContentIsNone(self):
        self.response_mock.json.return_value = None
        
        self.assertIsNone(reqcheck.get_pkg_info('test_pkg'))
    
    def testReturnsNoneWhenFailedToParseContent(self):
        self.response_mock.json.side_effect = ValueError()
        
        self.assertIsNone(reqcheck.get_pkg_info('test_pkg'))
    
    def testResultWithSuccess(self):
        self.response_mock.json.return_value = {'a':1}
        
        self.assertDictEqual({'a':1}, reqcheck.get_pkg_info('test_pkg'))

class GetPkgVersionsTest(unittest.TestCase):
    def setUp(self):
        self.get_pkg_info_patcher = mock.patch('reqcheck.get_pkg_info')
        self.get_pkg_info_mock = self.get_pkg_info_patcher.start()
    
    def testGetsPackageInfo(self):
        reqcheck.get_pkg_versions('test_pkg')
        
        self.get_pkg_info_mock.assert_called_with('test_pkg')
    
    def testReturnsEmptyListWhenFailedToGetPackageInfo(self):
        self.get_pkg_info_mock.return_value = None
        
        self.assertEqual([], reqcheck.get_pkg_versions('test_pkg'))
    
    def testReturnsEmptyListWhenReleasesNotSpecified(self):
        self.get_pkg_info_mock.return_value = {}
        
        self.assertEqual([], reqcheck.get_pkg_versions('test_pkg'))
    
    def testReturnsEmptyListWhenNoReleases(self):
        self.get_pkg_info_mock.return_value = {'releases': {}}
        
        self.assertEqual([], reqcheck.get_pkg_versions('test_pkg'))
    
    def testParsesAndSelectsLatestUploadTime(self):
        self.get_pkg_info_mock.return_value = {
            'releases': {
                '0.9': [{'upload_time': '2016-10-22T07:15:20'}],
                '1.0': [{'upload_time': '2016-10-22T12:07:15'}, {'upload_time': '2016-10-22T13:11:15'}],
                '1.1': [{'upload_time': '2016-10-23T14:51:50'}, {'upload_time': '2016-10-23T12:14:50'}],
            },
        }
        expected = [
            {'version': parse_version('0.9'), 'last_upload': datetime(2016, 10, 22, 7, 15, 20)},
            {'version': parse_version('1.0'), 'last_upload': datetime(2016, 10, 22, 13, 11, 15)},
            {'version': parse_version('1.1'), 'last_upload': datetime(2016, 10, 23, 14, 51, 50)},
        ]
        self.assertEqual(expected, reqcheck.get_pkg_versions('test_pkg'))
    
    def testIgnoreVersionsWithoutUploads(self):
        self.get_pkg_info_mock.return_value = {
            'releases': {
                '0.9': [{'upload_time': '2016-10-22T07:15:20'}],
                '1.0': [],
                '1.1': [{'upload_time': '2016-10-23T14:51:50'}],
            },
        }
        
        result = reqcheck.get_pkg_versions('test_pkg')
        
        expected = [parse_version(v) for v in ('0.9', '1.1')]
        self.assertEqual(expected, [row['version'] for row in result])
    
    def testSortedByVersion(self):
        self.get_pkg_info_mock.return_value = {
            'releases': {
                '0.9.1': [{'upload_time': '2016-10-22T07:15:20'}],
                '0.8.0': [{'upload_time': '2016-10-22T12:07:15'}],
                '0.9.0.rc1': [{'upload_time': '2016-10-23T14:51:50'}],
            },
        }
        
        result = reqcheck.get_pkg_versions('test_pkg')
        
        expected = [parse_version(v) for v in ('0.8.0', '0.9.0.rc1', '0.9.1')]
        self.assertEqual(expected, [row['version'] for row in result])

class GetVenvPipTest(unittest.TestCase):
    def setUp(self):
        self.venv_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        shutil.rmtree(self.venv_dir)
    
    def tempFile(self, *path):
        os.makedirs(os.path.join(self.venv_dir, *path[:-1]))
        with open(os.path.join(self.venv_dir, *path), 'w') as file:
            file.write('test_file')
    
    def testWithBinPip(self):
        self.tempFile('bin', 'pip')
        
        expected = os.path.join(self.venv_dir, 'bin', 'pip')
        self.assertEqual(expected, reqcheck.get_venv_pip(self.venv_dir))
    
    def testWithScriptsPipEXE(self):
        self.tempFile('Scripts', 'pip.exe')
        
        expected = os.path.join(self.venv_dir, 'Scripts', 'pip.exe')
        self.assertEqual(expected, reqcheck.get_venv_pip(self.venv_dir))
    
    def testWhenPipMissing(self):
        self.assertRaises(reqcheck.PipMissing, reqcheck.get_venv_pip, self.venv_dir)

class GetVenvPkgsTest(unittest.TestCase):
    def setUp(self):
        self.get_venv_pip_patcher = mock.patch('reqcheck.get_venv_pip')
        self.get_venv_pip_mock = self.get_venv_pip_patcher.start()
        
        self.popen_patcher = mock.patch('subprocess.Popen')
        self.popen_mock = self.popen_patcher.start()
        
        self.process_mock = mock.Mock()
        self.process_mock.returncode = 0
        self.process_mock.communicate.return_value = (None, None)
        self.popen_mock.return_value = self.process_mock
    
    def tearDown(self):
        self.get_venv_pip_patcher.stop()
        self.popen_patcher.stop()
    
    def testGetsVenvPip(self):
        reqcheck.get_venv_pkgs('/test/venv')
        
        self.get_venv_pip_mock.assert_called_with('/test/venv')
    
    def testStartsProcess(self):
        self.get_venv_pip_mock.return_value = '/test/venv/bin/pip'
        
        reqcheck.get_venv_pkgs('/test/venv')
        
        self.popen_mock.assert_called_with(
            ['/test/venv/bin/pip', '-q', 'freeze'],
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE
        )
    
    def testCommunicatesWithProcess(self):
        reqcheck.get_venv_pkgs('/test/venv')
        
        self.process_mock.communicate.assert_called_with()
    
    def testRaisesExceptionWhenNonZeroReturnCode(self):
        self.process_mock.returncode = 1
        
        self.assertRaises(reqcheck.PipFailed, reqcheck.get_venv_pkgs, '/test/venv')
    
    def testReturnsOutput(self):
        self.process_mock.communicate.return_value = ('test_output', None)
        
        self.assertEqual('test_output', reqcheck.get_venv_pkgs('/test/venv'))

class GetStdinPkgsTest(unittest.TestCase):
    def setUp(self):
        self.stdin_patcher = mock.patch('sys.stdin')
        self.stdin_mock = self.stdin_patcher.start()
    
    def tearDown(self):
        self.stdin_patcher.stop()
    
    def testReadsAndReturnsStdin(self):
        self.stdin_mock.read.return_value = 'test_stdin'
        
        self.assertEqual('test_stdin', reqcheck.get_stdin_pkgs())
        self.stdin_mock.read.assert_called_with()

class ParsePkgsTest(unittest.TestCase):
    def testReturnsEmptyListWhenNoPackages(self):
        self.assertEqual([], reqcheck.parse_pkgs(None))
        self.assertEqual([], reqcheck.parse_pkgs(''))
        self.assertEqual([], reqcheck.parse_pkgs(' \n\t\n'))
    
    def testParsesBasicPackageVersion(self):
        self.assertEqual([('test_pkg', parse_version('1.0.1'))], reqcheck.parse_pkgs('test_pkg==1.0.1'))
    
    def testSkipsBlankLines(self):
        pkgs = '''
pkg1==1.0.1

pkg2==1.0.2
   
'''
        expected = [('pkg1', parse_version('1.0.1')), ('pkg2', parse_version('1.0.2'))]
        self.assertEqual(expected, reqcheck.parse_pkgs(pkgs))
    
    def testReturnsPackageWithNoneVersionWhenVersionMissing(self):
        self.assertEqual([('test_pkg', None)], reqcheck.parse_pkgs('test_pkg'))

class GetAgeNumVersionsTest(unittest.TestCase):
    def setUp(self):
        self.versions = [
            {'version': parse_version('1.0.1')},
            {'version': parse_version('1.0.2')},
            {'version': parse_version('1.0.3')},
        ]
    
    def testWhenVersionNotFound(self):
        self.assertEqual(None, reqcheck.get_age_num_versions(self.versions, parse_version('1.0.1'), parse_version('5.1')))
        self.assertEqual(None, reqcheck.get_age_num_versions(self.versions, parse_version('5.1'), parse_version('1.0.1')))

class GetAgeTimeDeltaTest(unittest.TestCase):
    def setUp(self):
        self.versions = [
            {'version': parse_version('1.0.1'), 'last_upload': datetime(2016, 10, 22, 12, 34, 56)},
            {'version': parse_version('1.0.2'), 'last_upload': datetime(2016, 10, 22, 14, 46, 24)},
        ]
    
    def testWhenMissingVersion(self):
        self.assertEqual(None, reqcheck.get_age_time_delta(self.versions, parse_version('1.0.1'), None))
        self.assertEqual(None, reqcheck.get_age_time_delta(self.versions, None, parse_version('1.0.2')))
    
    def testWhenVersionsMatch(self):
        version = parse_version('1.0.1')
        self.assertEqual(timedelta(0), reqcheck.get_age_time_delta(self.versions, version, version))
    
    def testResult(self):
        expected = self.versions[1]['last_upload'] - self.versions[0]['last_upload']
        self.assertEqual(expected, reqcheck.get_age_time_delta(self.versions, parse_version('1.0.1'), parse_version('1.0.2')))

class NumVersionsToStrTest(unittest.TestCase):
    def testWithNone(self):
        self.assertEqual('unknown', reqcheck.num_versions_to_str(None))
    
    def testWithLessThanZero(self):
        self.assertEqual('unknown', reqcheck.num_versions_to_str(-1))
    
    def testWithZero(self):
        self.assertEqual('same version', reqcheck.num_versions_to_str(0))
    
    def testWithOne(self):
        self.assertEqual('-1 version', reqcheck.num_versions_to_str(1))
    
    def testWithMoreThanOne(self):
        self.assertEqual('-2 versions', reqcheck.num_versions_to_str(2))

class TimeDeltaToStrTest(unittest.TestCase):
    def testWithNone(self):
        self.assertEqual('unknown', reqcheck.timedelta_to_str(None))
    
    def testWhenLessThanOneDay(self):
        self.assertEqual('< 1 day', reqcheck.timedelta_to_str(timedelta(minutes = 30)))
    
    def testResultWithAllUnits(self):
        self.assertEqual('~ 2 years 3 days', reqcheck.timedelta_to_str(timedelta(days = 733, minutes = 2)))
    
    def testSingularEndings(self):
        self.assertEqual('~ 1 day', reqcheck.timedelta_to_str(timedelta(days = 1)))
        self.assertEqual('~ 1 year', reqcheck.timedelta_to_str(timedelta(days = 365)))

class CheckPkgsTest(unittest.TestCase):
    def setUp(self):
        self.get_pkg_versions_patcher = mock.patch('reqcheck.get_pkg_versions')
        self.get_pkg_versions_mock = self.get_pkg_versions_patcher.start()
        self.get_pkg_versions_mock.return_value = []
    
    def tearDown(self):
        self.get_pkg_versions_patcher.stop()
    
    def testWithEmptyPkgs(self):
        self.assertEqual([], reqcheck.check_pkgs(None))
        self.assertEqual([], reqcheck.check_pkgs(''))
        self.assertEqual([], reqcheck.check_pkgs(' \n \t  '))
    
    def testGetsPackageVersions(self):
        reqcheck.check_pkgs('pkg1==1.0.1\npkg2==1.0.2')
        
        self.get_pkg_versions_mock.assert_has_calls([mock.call('pkg1'), mock.call('pkg2')])
    
    def testResults(self):
        self.get_pkg_versions_mock.side_effect = iter([
            [
                {'version': parse_version('1.0.0'), 'last_upload': datetime(2014, 10, 21, 17, 14, 45)},
                {'version': parse_version('1.0.1'), 'last_upload': datetime(2016, 10, 22, 14, 14, 45)},
                {'version': parse_version('1.0.2'), 'last_upload': datetime(2016, 10, 22, 16, 14, 45)},
            ], [
                
                {'version': parse_version('2.0.0'), 'last_upload': datetime(2014, 10, 19, 11, 14, 45)},
                {'version': parse_version('2.0.1'), 'last_upload': datetime(2016, 10, 20, 14, 14, 45)},
                {'version': parse_version('2.0.2'), 'last_upload': datetime(2016, 10, 20, 16, 14, 45)},
            ], [
                
                {'version': parse_version('3.0.0'), 'last_upload': datetime(2014, 10, 19, 11, 14, 45)},
                {'version': parse_version('3.0.1'), 'last_upload': datetime(2016, 10, 20, 14, 14, 45)},
                {'version': parse_version('3.0.2'), 'last_upload': datetime(2016, 10, 20, 16, 14, 45)},
            ]
        ])
        expected = [
            {
                'pkg_name': 'pkg1',
                'current_version': parse_version('1.0.0'),
                'latest_version': parse_version('1.0.2'),
                'age_num_versions': 2,
                'age_time_delta': timedelta(days = 731, hours = 23),
                'age_str': '-2 versions (~ 2 years 1 day)',
            }, {
                'pkg_name': 'pkg2',
                'current_version': parse_version('2.0.1'),
                'latest_version': parse_version('2.0.2'),
                'age_num_versions': 1,
                'age_time_delta': timedelta(hours = 2),
                'age_str': '-1 version (< 1 day)',
            }, {
                'pkg_name': 'pkg3',
                'current_version': parse_version('3.0.2'),
                'latest_version': parse_version('3.0.2'),
                'age_num_versions': 0,
                'age_time_delta': timedelta(0),
                'age_str': 'latest',
            },
        ]
        self.assertEqual(expected, reqcheck.check_pkgs('pkg1==1.0.0\npkg2==2.0.1\npkg3==3.0.2'))

class CapturedIO(object):
    def __init__(self, channel, initial_value = None):
        self.channel = channel
        self.initial_value = initial_value
    
    def __enter__(self):
        self._backup = getattr(sys, self.channel)
        self.captured = six.StringIO(self.initial_value)
        setattr(sys, self.channel, self.captured)
        return self
    
    def __exit__(self, *args):
        setattr(sys, self.channel, self._backup)
    
    def read(self):
        return self.captured.getvalue()
    
    def write(self, data):
        self.captured.write(data)

class PrintResultsTest(unittest.TestCase):
    def setUp(self):
        self.tabulate_patcher = mock.patch('tabulate.tabulate')
        self.tabulate_mock = self.tabulate_patcher.start()
        self.tabulate_mock.return_value = 'test_output'
        self.results = [
            {
                'pkg_name': 'pkg2',
                'current_version': parse_version('2.0.0'),
                'latest_version': parse_version('2.0.2'),
                'age_str': '-2 versions (~ 2 years 1 day)',
            }, {
                'pkg_name': 'pkg1',
                'current_version': parse_version('1.0.0'),
                'latest_version': parse_version('1.0.2'),
                'age_str': '-2 versions (< 1 day)',
            }, {
                'pkg_name': 'pkg3',
                'current_version': parse_version('3.0.0'),
                'latest_version': parse_version('3.0.2'),
                'age_str': '-2 versions (~ 3 years 2 days)',
            },
        ]
    
    def tearDown(self):
        self.tabulate_patcher.stop()
    
    def testCallsTabulateToProduceOutput(self):
        with CapturedIO('stdout'):
            reqcheck.print_results(self.results)
        
        # Table is sorted by pkg_name
        expected_table = [
            ('pkg1', parse_version('1.0.0'), parse_version('1.0.2'), '-2 versions (< 1 day)'),
            ('pkg2', parse_version('2.0.0'), parse_version('2.0.2'), '-2 versions (~ 2 years 1 day)'),
            ('pkg3', parse_version('3.0.0'), parse_version('3.0.2'), '-2 versions (~ 3 years 2 days)'),
        ]
        expected_headers = ['Package', 'Current Version', 'Latest Version', 'Age']
        self.tabulate_mock.assert_called_with(expected_table, headers = expected_headers)
    
    def testPrintsOutputToScreen(self):
        with CapturedIO('stdout') as captured:
            reqcheck.print_results(self.results)
            self.assertEqual('test_output', captured.read())

class CmdlineTest(unittest.TestCase):
    def setUp(self):
        self.check_pkgs_patcher = mock.patch('reqcheck.check_pkgs')
        self.check_pkgs_mock = self.check_pkgs_patcher.start()
        
        self.print_results_patcher = mock.patch('reqcheck.print_results')
        self.print_results_mock = self.print_results_patcher.start()
        
        self.results = [{}, {}, {}]
        self.check_pkgs_mock.return_value = self.results
    
    def tearDown(self):
        self.check_pkgs_patcher.stop()
        self.print_results_patcher.stop()
    
    def testExitsWithErrorCodeAndPrintsToStderrWhenCommandLineError(self):
        with CapturedIO('stderr') as captured:
            self.assertRaises(SystemExit, reqcheck.cmdline, ['-bad', 'param'])
            self.assertTrue(len(captured.read()) > 0)
    
    def testWithPkgsOnCommandLine(self):
        reqcheck.cmdline(['pkg1==1.0.0', 'pkg2==1.0.1'])
        
        self.check_pkgs_mock.assert_called_with('pkg1==1.0.0\npkg2==1.0.1')
    
    @mock.patch('reqcheck.get_venv_pkgs', )
    def testWithVenv(self, get_venv_pkgs_mock):
        pkgs = 'pkg1==1.0.1\npkg2==2.0.1'
        get_venv_pkgs_mock.return_value = pkgs
        
        reqcheck.cmdline(['-v', '/test/venv'])
        
        get_venv_pkgs_mock.assert_called_with('/test/venv')
        self.check_pkgs_mock.assert_called_with(pkgs)
    
    def testWithStdin(self):
        pkgs = 'pkg1==1.1\npkg2==1.2'
        
        with CapturedIO('stdin', pkgs) as captured:
            reqcheck.cmdline([])
        
        self.check_pkgs_mock.assert_called_with(pkgs)
    
    def testPrintsResults(self):
        reqcheck.cmdline(['pkg1==1.0.0', 'pkg2==1.0.1'])
        
        self.print_results_mock.assert_called_with(self.results)
