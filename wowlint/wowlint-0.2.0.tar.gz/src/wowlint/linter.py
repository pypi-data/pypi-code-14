import os

from construct.core import ConstructError

from wowlint.validation.common import LINT_CLASSES as COMMON_LINT_CLASSES
from wowlint.validation.core import Severity, Issue
from wowlint.validation.liturgy import LINT_CLASSES as LITURGY_LINT_CLASSES
from wowlint.validation.songs import LINT_CLASSES as SONG_LINT_CLASSES
from wowlint.wowfile import Resource


class Linter(object):

    KNOWN_EXTENSIONS = ['.wsg', '.wow-song', '.wlt', '.wow-liturgy']

    def __init__(self, minSeverity=None, config={}):
        self.minSeverity = minSeverity

        commonLints = map(lambda l: l(config.get(l.__name__, {})), COMMON_LINT_CLASSES)

        self.lints = {
            'Song Words': map(lambda l: l(config.get(l.__name__, {})), SONG_LINT_CLASSES) + commonLints,
            'Liturgy': map(lambda l: l(config.get(l.__name__, {})), LITURGY_LINT_CLASSES) + commonLints
        }

    def lint(self, filename):
        issues = []
        ext = os.path.splitext(filename)[1]
        if ext in self.KNOWN_EXTENSIONS:
            with open(filename, "rb") as f:
                try:
                    model = Resource.parse(f.read())
                    for lint in self.lints.get(model.filetype, []):
                        if lint.severity >= self.minSeverity and self._shouldLintFile(lint, filename):
                            issues += lint.validate(model)
                except ConstructError as e:
                    Issue(Severity.FATAL, "{} Not a valid Words of Worship file".format(e.__class__.__name__)).add_to(issues)
        else:
            Issue(Severity.INFO, "Unrecognised file extension: {}".format(ext)).add_to(issues)
        return issues

    def _shouldLintFile(self, lint, filename):
        if "exclude" in lint.config and filename in lint.config["exclude"]:
            return False
        return True
