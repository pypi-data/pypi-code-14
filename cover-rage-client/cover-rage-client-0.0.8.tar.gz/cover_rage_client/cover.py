import datetime
import os
from collections import OrderedDict
from subprocess import Popen, PIPE
from typing import List

import xmltodict


ListOfStrings = List[str]
ListOfTuples = List[tuple]


MAX_COVERAGE = 1.0
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
SHOW_LINE_NUM_AWK_SCRIPT_PATH = os.path.join(PROJECT_ROOT, 'utils', 'showlinenum.awk')
NEW_LINES_SCRIPT_PATH = os.path.join(PROJECT_ROOT, 'utils', 'newlines.sh')


# TODO: rewrite it on pure Python
def git_new_lines(git_root: str) -> dict:
    assert os.path.exists(git_root)
    assert os.path.isdir(git_root)
    process = Popen(
        ['/bin/bash', NEW_LINES_SCRIPT_PATH, SHOW_LINE_NUM_AWK_SCRIPT_PATH],
        cwd=git_root,
        stdout=PIPE,
        stderr=PIPE
    )
    out, error = process.communicate()
    exit_code = process.wait()
    assert exit_code == 0, error
    assert error == b'', error
    new_lines = {}
    for line in out.decode("utf-8").split('\n'):
        if len(line) > 1:
            fname, line_num = line.split(':')
            line_num = int(line_num)
            if fname in new_lines:
                new_lines[fname].append(line_num)
            else:
                new_lines[fname] = [line_num]
    return new_lines


class ParseCoverageXmlError(Exception):

    pass


class PythonFile(object):

    """
    Representation of Python file coverage (in terms of `Cobertura` it's not a file - it's a class)

    <xml>
        ...
        <packages>
            <package line-rate="0.98" name=".">
                <classes>
                    <class filename="file1.py" line-rate="1" name="file1.py">
                        <lines>
                            <line hits="1" number="2"/>
                            <line hits="1" number="3"/>
                            ...
                        </lines>
                    </class>
                </classes>
            </package>
            ...
        </packages>
    </xml>
    """

    lines = []

    def __init__(self, xml_class: str) -> None:
        assert '@filename' in xml_class
        assert '@name' in xml_class
        assert '@line-rate' in xml_class
        assert 'lines' in xml_class

        self.filename = xml_class['@filename']
        self.name = xml_class['@name']
        try:
            self.line_rate = float(xml_class['@line-rate'])
        except ValueError as e:
            raise ParseCoverageXmlError(e)

        if xml_class['lines']:
            assert 'line' in xml_class['lines']
            self.lines = self.get_lines(xml_class['lines']['line'])

    @staticmethod
    def get_lines(xml_lines: OrderedDict) -> ListOfTuples:
        if isinstance(xml_lines, OrderedDict):
            xml_lines = [xml_lines]
        else:
            assert hasattr(xml_lines, '__iter__')
        try:
            lines = [(int(xml_line['@number']), int(xml_line['@hits'])) for xml_line in xml_lines]
        except ValueError as e:
            raise ParseCoverageXmlError(e)
        return lines

    @property
    def uncovered_lines(self) -> ListOfStrings:
        if self.line_rate == MAX_COVERAGE:
            return []
        else:
            return [line[0] for line in self.lines if line[1] == 0]


class PythonPackage(object):

    """
    Representation of Python package coverage

    <xml>
        ...
        <packages>
            <package line-rate="0.98" name=".">
                <classes>
                    <class filename="file1.py" line-rate="1" name="file1.py">...</class>
                    <class filename="file2.py" line-rate="0.96" name="file2.py">...</class>
                </classes>
            </package>
            ...
        </packages>
    </xml>
    """

    classes = []

    def __init__(self, xml_package: str) -> None:
        assert '@name' in xml_package
        self.name = xml_package['@name']
        try:
            self.line_rate = float(xml_package['@line-rate'])
        except ValueError as e:
            raise ParseCoverageXmlError(e)
        assert 'classes' in xml_package
        if xml_package['classes']:
            assert 'class' in xml_package['classes']
            self.classes = self.get_classes(xml_package['classes']['class'])

    @staticmethod
    def get_classes(xml_classes: OrderedDict) -> ListOfStrings:
        if isinstance(xml_classes, OrderedDict):
            xml_classes = [xml_classes]
        else:
            assert hasattr(xml_classes, '__iter__')
        return [PythonFile(xml_class) for xml_class in xml_classes]


class PythonCoverage(object):

    """
    Representation of all project coverage

    <xml>
        <coverage line-rate="0.99" timestamp="1467374597147" version="4.1">
        ...
        <packages>
            <package line-rate="1" name=".">...</package>
            <package complexity="0" line-rate="0.99" name="apps.app1">...</package>
            <package complexity="0" line-rate="0.98" name="apps.app2">...</package>
        </packages>
    </xml>
    """

    COVERAGE_FILE_NAME = 'coverage.xml'
    packages = []

    def __init__(self, project_directory: str, xml_filename: str) -> None:
        assert os.path.exists(project_directory)
        assert os.path.isdir(project_directory)
        assert os.path.exists(xml_filename)
        assert os.path.isfile(xml_filename)

        self.project_directory = project_directory

        # Read data from `coverage.xml` file
        # http://coverage.readthedocs.io/en/coverage-4.1/cmd.html#xml-reporting
        with open(xml_filename, 'r') as fd:
            raw_data = xmltodict.parse(fd.read())

        assert raw_data
        assert 'coverage' in raw_data
        assert 'packages' in raw_data['coverage']
        assert '@line-rate' in raw_data['coverage']
        assert '@version' in raw_data['coverage']
        assert '@timestamp' in raw_data['coverage']
        assert 'package' in raw_data['coverage']['packages']

        try:
            self.line_rate = float(raw_data['coverage']['@line-rate'])
            self.timestamp = datetime.datetime.utcfromtimestamp(int(raw_data['coverage']['@timestamp']) // 1000)
        except ValueError as e:
            raise ParseCoverageXmlError(e)
        self.version = raw_data['coverage']['@version']
        self.packages = self.get_packages(raw_data['coverage']['packages']['package'])

    @staticmethod
    def get_packages(xml_packages: OrderedDict) -> ListOfStrings:
        if isinstance(xml_packages, OrderedDict):
            xml_packages = [xml_packages]
        else:
            assert hasattr(xml_packages, '__iter__')
        return [PythonPackage(xml_package) for xml_package in xml_packages]

    @property
    def uncovered_lines(self) -> dict:
        uncovered = {}
        for package in self.packages:
            for klass in package.classes:
                if klass.line_rate < MAX_COVERAGE:
                    uncovered[klass.filename] = [line for line in klass.uncovered_lines]
        return uncovered

    def compare_coverage_with_diff(self, diff=None, directory=None) -> dict:
        if diff is None:
            if directory is None:
                directory = self.project_directory
            diff = git_new_lines(directory)
        new_uncovered_lines = {}
        for k, v in diff.items():
            uncovered_key = None
            for u in self.uncovered_lines.keys():
                if u in k:
                    uncovered_key = u
                    break
            if uncovered_key:
                uncovered = set(self.uncovered_lines[uncovered_key]) & set(v)
                if uncovered:
                    new_uncovered_lines[k] = list(uncovered)
                    new_uncovered_lines[k].sort()
        return new_uncovered_lines
