from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import sys

from pip.req import parse_requirements


class UnpinnedVersionFoundException(Exception):
    pass


def parse_pinned_versions(req_file):
    result = {}
    for req in parse_requirements(req_file, session=object):
        result[req.name] = req.is_pinned
    return result


def display_unpinned_requirements(pinned_or_not):
    for req_name, is_pinned in pinned_or_not.items():
        if not is_pinned:
            msg = '"{req_name}" should be pinned.'.format(req_name=req_name)
            printout(msg)


def get_requirements_files(params):
    if len(params) == 0:
        req_files = [os.path.join(os.getcwd(), 'requirements.txt')]
    else:
        req_files = params

    abs_req_files = []
    for req_file in req_files:
        if os.path.isabs(req_file):
            abs_req_files.append(req_file)
        else:
            abs_req_file = os.path.abspath(os.path.join(os.getcwd(), req_file))
            abs_req_files.append(abs_req_file)

    for abs_req_file in abs_req_files:
        assert os.path.exists(abs_req_file)
        assert os.path.isfile(abs_req_file)

    return abs_req_files


def handle_one_file(reqquirements_file):
    printout('verifying requirements file "{0}"'.format(reqquirements_file))
    pinned_or_not = parse_pinned_versions(reqquirements_file)
    display_unpinned_requirements(pinned_or_not)
    contains_unpinned_reqs = not all(pinned_or_not.values())

    if contains_unpinned_reqs:
        printout('Error. One or more requirement is not pinned.')
        raise UnpinnedVersionFoundException()


def printout(msg):
    print(msg)


def get_argv():
    return sys.argv[:1]


def exit_program(code=None):
    sys.exit(code)


def main():
    unpinned_seen = False
    for req_file in get_requirements_files(get_argv()):
        try:
            handle_one_file(req_file)
        except UnpinnedVersionFoundException:
            unpinned_seen = True

    printout('Done.')
    if unpinned_seen:
        exit_program(1)
