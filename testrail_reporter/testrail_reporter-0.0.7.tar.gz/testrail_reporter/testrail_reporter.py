from __future__ import print_function
from pprint import pprint
from sys import exit
from textwrap import dedent
from warnings import warn

from nose.plugins import Plugin
from nose.suite import ContextSuite
from testrail import TestRail

class TestRailReporter(Plugin):
    '''
    Automatically Publish Test Results to TestRail
    Requires --testrail_api_key, --testrail_email, --testrail_project_id,
    --testrail_url, --testrail_plan_name
    '''

    # setup Nose Plugin
    def options(self, parser, env):
        super(TestRailReporter, self).options(parser, env)
        parser.add_option('--testrail_api_key', dest='api_key',
                          help='API Key provided by TestRail')
        parser.add_option('--testrail_debug_results', dest='debug_results',
                          help=dedent('''Dump results to screen before trying
                                      to push results to TestRail.'''))
        parser.add_option('--testrail_email', dest='email',
                          help='The email address you use to sign in to Testrail')
        parser.add_option('--testrail_error_id', dest='error_id',
                          help=dedent('''If you use a custom id for errors,
                                      enter it here. Defaults to 5
                                      (failure).'''))
        parser.add_option('--testrail_milestone_name', dest='milestone_name',
                          help=dedent('''Name of the TestRail Milestone you
                                      want to associate with current TestRail
                                      Test Plan'''))
        parser.add_option('--testrail_no_catchall', dest='no_catchall',
                          help=dedent('''If no suite or section ID can be
                                      determined, DO NOT create a default
                                      "catchall". Will result in test cases NOT
                                      being created if suite or section ID is
                                      missing.'''))
        parser.add_option('--testrail_project_id', dest='project_id',
                          help='The TestRail Project ID for this project.')
        parser.add_option('--testrail_plan_name', dest='plan_name',
                          help='The name of the TestRail test plan.')
        parser.add_option('--testrail_skip_id', dest='skip_id',
                          help=dedent('''If you use a custom id for skips,
                                      enter it here. Defaults to 1
                                      (pass).'''))
        parser.add_option('--testrail_url', dest='url',
                          help=dedent('''The URL you use to access TestRail EG
                                      https://company_name.testrail.com'''))

    def configure(self, options, conf):
        super(TestRailReporter, self).configure(options, conf)
        self.client = None
        if not self.enabled:
            return
        self.api_key        = options.api_key
        self.debug_results  = bool(options.debug_results)
        self.email          = options.email
        self.error_id       = int(options.error_id or 5)
        self.milestone_name = options.milestone_name
        self.no_catchall    = bool(options.no_catchall)
        self.project_id     = int(options.project_id or -1)
        self.plan_name      = options.plan_name
        self.skip_id        = int(options.skip_id or 1)
        self.url            = options.url

        if  self.url \
        and self.email \
        and self.api_key \
        and self.plan_name \
        and self.project_id >= 0:
            self.client = TestRail(project_id=self.project_id, email=self.email,
                                   key=self.api_key, url=self.url).api
        else:
            warning = dedent('''
                !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                ! NOTHING WILL BE REPORTED TO TESTRAIL !
                !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                You specified --with-testrailreporter
                This requires the following options:
                --testrail_api_key    current value: {api}
                --testrail_email      current value: {email}
                --testrail_project_id current value: {pid}
                --testrail_plan_name  current value: {plan}
                --testrail_url        current value: {url}
                ''')
            warning = warning.format(api=self.api_key, email=self.email,
                                     pid=self.project_id, plan=self.plan_name,
                                     url=self.url)
            warn(warning)

    # Nose plugin methods
    def addError(self, test, err):
        self.collect_result(test, self.error_id)

    def addFailure(self, test, err):
        self.collect_result(test, 5)

    def addSkipped(self, test):
        warn('skipped test: {}'.format(test))
        self.collect_result(test, self.skip_id)

    def addSuccess(self, test):
        self.collect_result(test, 1)

    def begin(self):
        self.cache   = dict()
        self.results = dict()
        self.cache_suites()
        self.cache_sections()
        self.cache_cases()

    def finalize(self, result):
        if self.client is not None:
            self.publish_results()

    # internal methods
    def cache_cases(self):
        cases = dict()
        for suite_id in self.cache['suites'].values():
            for case in self.client.cases(project_id=self.project_id,
                                          suite_id=suite_id):
                cases[case['title']] = case['id']
        self.cache['cases'] = cases

    def cache_sections(self):
        sections = dict()
        for suite_id in self.cache['suites'].values():
            for section in self.client.sections(project_id=self.project_id,
                                                suite_id=suite_id):
                if sections.get(suite_id, None) is None:
                    sections[suite_id] = dict()
                sections[suite_id][section['name']] = section['id']
        self.cache['sections'] = sections

    def cache_suites(self):
        suites = dict()
        for suite in self.client.suites(self.project_id):
            suites[suite['name']] = suite['id']
        self.cache['suites'] = suites

    def catchall_warning(self, suite_or_section, test):
        case_title = self.extract_case_title(test)
        warning = dedent('''Unable to determine {} for test case {}.
                         --testrail_no_catchall is set, so this case will not
                         be added to TestRail.'''.format(suite_or_section,
                                                         case_title))
        warn(warning)

    def collect_result(self, test, status_id):
        if self.client is None:
            return
        if type(test) == ContextSuite:
            return
        if hasattr(test, 'test'):
            test = test.test
        suite_id = self.fetch_suite_id(test)
        if suite_id is None:
            return
        if self.results.get(suite_id, None) is None:
            self.results[suite_id] = dict()
        section_id = self.fetch_section_id(test, suite_id)
        if section_id is None:
            return
        case_id = self.fetch_case_id(test, suite_id, section_id)
        self.results[suite_id][case_id] = dict(section_id=section_id,
                                               status_id=status_id)

    def create_case(self, title, section_id):
        payload = dict(title=title, section_id=section_id)
        case_id = self.client.add_case(payload)['id']
        self.cache['cases'][title] = case_id
        return case_id

    def create_milestone(self):
        payload = dict(name=self.milestone_name, project_id=self.project_id)
        return self.client.add_milestone(payload)['id']

    def create_plan(self):
        payload = dict(name=self.plan_name, project_id=self.project_id)
        if self.milestone_name is not None:
            payload.update(milestone_id=self.fetch_milestone_id())
        return self.client.add_plan(payload)['id']

    def create_plan_entry(self, plan_id, suite_id):
        payload = dict(plan_id=plan_id, suite_id=suite_id)
        entry = self.client.add_plan_entry(payload)
        return entry['runs'][-1]['id']

    def create_section(self, name, suite_id):
        payload = dict(name=name, suite_id=suite_id, project_id=self.project_id)
        section_id = self.client.add_section(payload)['id']
        self.cache['sections'][suite_id][name] = section_id
        return section_id

    def create_suite(self, name):
        payload = dict(name=name, project_id=self.project_id)
        suite_id = self.client.add_suite(payload)['id']
        self.cache['suites'][name] = suite_id
        self.cache['sections'][suite_id] = dict()
        return suite_id

    def extract_case_title(self, test):
        if type(test._testMethodDoc) == str:
            return test._testMethodDoc.split('\n')[0]
        return test.id()

    def fetch_case_id(self, test, suite_id, section_id):
        if not self.cache.has_key('cases'):
            self.cache_cases()
        case_title = self.extract_case_title(test)
        case_id = self.cache['cases'].get(case_title, None)
        if case_id is not None:
            return case_id
        return self.create_case(case_title, section_id)

    def fetch_milestone_id(self):
        for milestone in self.client.milestones(project_id=self.project_id):
            if  milestone['name'] == self.milestone_name \
            and not bool(milestone['is_completed']):
                return milestone['id']
        return self.create_milestone()

    def fetch_plan_id(self):
        for plan in self.client.plans(self.project_id):
            if plan['name'] == self.plan_name and not bool(plan['is_completed']):
                return plan['id']
        return self.create_plan()

    def fetch_section_id(self, test, suite_id):
        if not self.cache.has_key('sections'):
            self.cache_sections()
        section_name = getattr(test, 'section_name', 'catchall')

        section_id = self.cache['sections'][suite_id].get(section_name, None)
        if section_id is not None:
            return section_id
        if section_name == 'catchall' and self.no_catchall:
            self.catchall_warning('section', test)
            return None
        return self.create_section(section_name, suite_id)

    def fetch_suite_id(self, test):
        if not self.cache.has_key('suites'):
            self.cache_suites()
        suite_name = getattr(test, 'suite_name', 'catchall')
        suite_id = self.cache['suites'].get(suite_name, None)
        if suite_id is not None:
            return suite_id
        if suite_name == 'catchall' and self.no_catchall:
            self.catchall_warning('suite', test)
            return None
        return self.create_suite(suite_name)

    def fetch_tests(self, run_id):
        tests = dict()
        for test in self.client.tests(run_id):
            tests[test['case_id']] = test['id']
        return tests

    def generate_results(self, run_id, suite_id):
        tests = self.fetch_tests(run_id)
        results = list()
        for case_id in tests.keys():
            if self.results[suite_id].get(case_id, None) is not None:
                results.append(dict(test_id=tests[case_id],
                                    status_id=self.results[suite_id][case_id]['status_id']))
        return results

    def publish_results(self):
        plan_id = self.fetch_plan_id()
        for suite_id in self.results.keys():
            run_id = self.create_plan_entry(plan_id, suite_id)
            results = self.generate_results(run_id, suite_id)
            if self.debug_results:
                print('suite id: {}'.format(suite_id))
                pprint(results)
                print('-'*25)
            if len(results) > 0:
                self.client.add_results(results, run_id)
