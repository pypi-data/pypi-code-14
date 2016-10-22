import os
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "templateaddons.test_settings")
current_dirname = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(current_dirname, '..'))

import django  # NOQA
django.setup()

from django.test.runner import DiscoverRunner  # NOQA
from django.core.management import call_command  # NOQA


class TestSuiteRunner(DiscoverRunner):

    def run_tests(self, test_labels=('templateaddons',), extra_tests=None):
        results = DiscoverRunner.run_tests(self, test_labels, extra_tests)
        sys.exit(results)


def build_suite():
    runner = TestSuiteRunner()
    runner.setup_test_environment()
    runner.setup_databases()
    return runner.build_suite(test_labels=('templateaddons',), extra_tests=None)

if __name__ == '__main__':
    runner = TestSuiteRunner(failfast=False)
    if len(sys.argv) > 1:
        runner.run_tests(test_labels=(sys.argv[1], ))
    else:
        runner.run_tests()
