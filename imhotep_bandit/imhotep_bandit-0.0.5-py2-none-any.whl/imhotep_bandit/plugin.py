import re
import json
import os.path
import textwrap
from collections import defaultdict

from imhotep.tools import Tool


class Bandit(Tool):
    def invoke(self, dirname, filenames, linter_configs):
        retval = defaultdict(lambda: defaultdict(list))

        if filenames:
            files = ' '.join(filenames)
        else:
            files = '-r %s' % dirname

        cmd = 'bandit -f json %s' % files
        output = self.executor(cmd)
        data = json.loads(output.decode('utf8'))

        for result in data['results']:
            line = str(result['line_number'])
            message = self.format_message(result)
            retval[result['filename']][line].append(message)

        return self.to_dict(retval)

    def format_message(self, report):
        return textwrap.dedent("""
            **{test_id}**: {issue_text}
            Severity: {issue_severity}, Confidence: {issue_confidence}
        """.format(**report)).strip()

    def to_dict(self, d):
        if not isinstance(d, dict):
            return d

        return {
            k: self.to_dict(v) for k, v in d.items()
        }
