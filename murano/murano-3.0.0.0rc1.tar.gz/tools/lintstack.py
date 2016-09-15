#!/usr/bin/env python
# Copyright (c) 2015 OpenStack Foundation.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""pylint error checking."""

from __future__ import print_function

import json
import os
import re
import sys

from pylint import lint
from pylint.reporters import text
from six.moves import cStringIO as StringIO

# enabled checks
# http://pylint-messages.wikidot.com/all-codes
ENABLED_CODES = (
    # refactor category
    "R0801", "R0911", "R0912", "R0913", "R0914", "R0915",
    # warning category
    "W0612", "W0613", "W0703",
    # convention category
    "C1001")

LINE_PATTERN = r"(\S+):(\d+): \[(\S+)(, \S*)?] (.*)"

KNOWN_PYLINT_EXCEPTIONS_FILE = "tools/pylint_exceptions"


class LintOutput(object):

    _cached_filename = None
    _cached_content = None

    def __init__(self, filename, lineno, line_content, code, message,
                 lintoutput, additional_content):
        self.filename = filename
        self.lineno = lineno
        self.line_content = line_content
        self.code = code
        self.message = message
        self.lintoutput = lintoutput
        self.additional_content = additional_content

    @classmethod
    def get_duplicate_code_location(cls, remaining_lines):
        module, lineno = remaining_lines.pop(0)[2:].split(":")
        filename = module.replace(".", os.sep) + ".py"
        return filename, int(lineno)

    @classmethod
    def get_line_content(cls, filename, lineno):
        if cls._cached_filename != filename:
            with open(filename) as f:
                cls._cached_content = list(f.readlines())
                cls._cached_filename = filename
        # find first non-empty line
        lineno -= 1
        while True:
            line_content = cls._cached_content[lineno].rstrip()
            lineno += 1
            if line_content:
                return line_content

    @classmethod
    def from_line(cls, line, remaining_lines):
        m = re.search(LINE_PATTERN, line)
        if not m:
            return None
        matched = m.groups()
        filename, lineno, code, message = (matched[0], int(matched[1]),
                                           matched[2], matched[-1])
        additional_content = None

        # duplicate code output needs special handling
        if "duplicate-code" in code:
            line_count = 0
            for next_line in remaining_lines:
                if re.search(LINE_PATTERN, next_line):
                    break
                line_count += 1
            if line_count:
                additional_content = remaining_lines[0:line_count]

            filename, lineno = cls.get_duplicate_code_location(remaining_lines)
            # fixes incorrectly reported file path
            line = line.replace(matched[0], filename)
            line = line.replace(":%s:" % matched[1], "")

        line_content = cls.get_line_content(filename, lineno)
        return cls(filename, lineno, line_content, code, message,
                   line.rstrip(), additional_content)

    @classmethod
    def from_msg_to_dict(cls, msg):
        """Creates dict from pylint msg

        From the output of pylint msg, to a dict, where each key
        is a unique error identifier, value is a list of LintOutput
        """
        result = {}
        lines = msg.splitlines()
        while lines:
            line = lines.pop(0)
            obj = cls.from_line(line, lines)
            if not obj:
                continue
            key = obj.key()
            if key not in result:
                result[key] = []
            result[key].append(obj)
        return result

    def key(self):
        return self.message, self.line_content.strip()

    def json(self):
        return json.dumps(self.__dict__)

    def review_str(self):
        kargs = {"filename": self.filename,
                 "lineno": self.lineno,
                 "line_content": self.line_content,
                 "code": self.code,
                 "message": self.message}
        return ("File %(filename)s\nLine %(lineno)d:%(line_content)s\n"
                "%(code)s: %(message)s" % kargs)


class ErrorKeys(object):

    @classmethod
    def print_json(cls, errors, output=sys.stdout):
        print("# automatically generated by tools/lintstack.py", file=output)
        for i in sorted(errors.keys()):
            print(json.dumps(i), file=output)

    @classmethod
    def from_file(cls, filename):
        keys = set()
        for line in open(filename):
            if line and line[0] != "#":
                d = json.loads(line)
                keys.add(tuple(d))
        return keys


def run_pylint():
    buff = StringIO()
    reporter = text.ParseableTextReporter(output=buff)
    args = ["-rn", "--disable=all", "--enable=" + ",".join(ENABLED_CODES),
            "murano"]
    lint.Run(args, reporter=reporter, exit=False)
    val = buff.getvalue()
    buff.close()
    return val


def generate_error_keys(msg=None):
    print("Generating", KNOWN_PYLINT_EXCEPTIONS_FILE)
    if msg is None:
        msg = run_pylint()

    errors = LintOutput.from_msg_to_dict(msg)
    with open(KNOWN_PYLINT_EXCEPTIONS_FILE, "w") as f:
        ErrorKeys.print_json(errors, output=f)


def validate(newmsg=None):
    print("Loading", KNOWN_PYLINT_EXCEPTIONS_FILE)
    known = ErrorKeys.from_file(KNOWN_PYLINT_EXCEPTIONS_FILE)
    if newmsg is None:
        print("Running pylint. Be patient...")
        newmsg = run_pylint()
    errors = LintOutput.from_msg_to_dict(newmsg)

    print()
    print("Unique errors reported by pylint: was %d, now %d."
          % (len(known), len(errors)))
    passed = True
    for err_key, err_list in errors.items():
        for err in err_list:
            if err_key not in known:
                print()
                print(err.lintoutput)
                print(err.review_str())
                if err.additional_content:
                    max_len = max(map(len, err.additional_content))
                    print("-" * max_len)
                    print(os.linesep.join(err.additional_content))
                    print("-" * max_len)
                passed = False
    if passed:
        print("Congrats! pylint check passed.")
        redundant = known - set(errors.keys())
        if redundant:
            print("Extra credit: some known pylint exceptions disappeared.")
            for i in sorted(redundant):
                print(json.dumps(i))
            print("Consider regenerating the exception file if you will.")
    else:
        print()
        print("Please fix the errors above. If you believe they are false "
              "positives, run 'tools/lintstack.py generate' to overwrite.")
        sys.exit(1)


def usage():
    print("""Usage: tools/lintstack.py [generate|validate]
    To generate pylint_exceptions file: tools/lintstack.py generate
    To validate the current commit: tools/lintstack.py
    """)


def main():
    option = "validate"
    if len(sys.argv) > 1:
        option = sys.argv[1]
    if option == "generate":
        generate_error_keys()
    elif option == "validate":
        validate()
    else:
        usage()


if __name__ == "__main__":
    main()
