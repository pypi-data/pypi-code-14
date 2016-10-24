from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import sys


class UnpinnedVersionFoundException(Exception):
    pass


def get_content(req_file):
    with open(req_file) as f:
        for line in f:
            yield line


def parse_pinned_versions(req_file):
    result = {}

    req_file_content = get_content(req_file)
    for line in req_file_content:
        # skips comments and empty lines.
        print(line)
        req = line.split('#')[0].strip()
        if req.startswith('-r'):
            result.update(parse_pinned_versions(req.split('-r')[1].strip()))
            continue
        if len(req) == 0:
            continue
        pinned = is_pinned(req)
        result[req] = pinned
    return result


def is_pinned(req):
    req_no_comments = req.split('#')[0]
    if '==' in req_no_comments and '*' not in req_no_comments.split('==')[1]:
        return True
    return False


def display_unpinned_requirements(pinned_or_not):
    for req_name, is_pinned in pinned_or_not.items():
        if not is_pinned:
            msg = '"{req_name}" should be pinned.'.format(req_name=req_name)
            print(msg)


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
        print(abs_req_file)
        assert os.path.exists(abs_req_file)
        assert os.path.isfile(abs_req_file)

    return abs_req_files


def handle_one_file(requirements_file):
    print('verifying requirements file "{0}"'.format(requirements_file))

    pinned_or_not = parse_pinned_versions(requirements_file)

    display_unpinned_requirements(pinned_or_not)
    contains_unpinned_reqs = not all(pinned_or_not.values())

    if contains_unpinned_reqs:
        print('Error. One or more requirement is not pinned.')
        raise UnpinnedVersionFoundException()


def get_argv():
    return sys.argv[1:]


def exit_program(code=None):
    sys.exit(code)


def main():
    unpinned_seen = False
    for req_file in get_requirements_files(get_argv()):
        try:
            handle_one_file(req_file)
        except UnpinnedVersionFoundException:
            unpinned_seen = True

    print('Done.')
    if unpinned_seen:
        exit_program(1)
