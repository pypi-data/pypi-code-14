from wowlint.validation.core import Severity, Lint, LinewiseLint
from wowlint.wowfile import LicenseType, LineType


class HasNoCopyright(Lint):
    message = "No copyright details provided"
    severity = Severity.ERROR

    def validate_resource(self, song):
        if song.content.copyright == "" and (not song.content.license or song.content.license.type == LicenseType.CCL):
            return [self.create_issue()]


class HasNoAuthor(Lint):
    message = "No author provided"
    severity = Severity.ERROR

    def validate_resource(self, song):
        if song.content.author == "":
            return [self.create_issue()]


class AllMinorWords(Lint):
    message = "Entirely uses minor words"
    severity = Severity.WARNING

    def validate_resource(self, song):
        for block in song.content.block:
            for line in block.line:
                if line.type == LineType.NORMAL:
                    return None
        return [self.create_issue()]


class TrailingComma(LinewiseLint):
    message = "({block}:{line}) Line has trailing comma"
    severity = Severity.WARNING

    def validate_line(self, blockIndex, lineIndex, line):
        if line.text.endswith(","):
            return [self.create_issue(blockIndex, lineIndex)]


class NoInitialCapital(LinewiseLint):
    message = "({block}:{line}) Line does not start with a capital letter"
    severity = Severity.WARNING

    def validate_line(self, blockIndex, lineIndex, line):
        if line.text[0] != line.text[0].upper():
            return [self.create_issue(blockIndex, lineIndex)]


LINT_CLASSES = [
    HasNoCopyright,
    HasNoAuthor,
    TrailingComma,
    NoInitialCapital,
    AllMinorWords
]
