from enum import Enum


class Severity(Enum):
    INFO = 0
    WARNING = 1
    ERROR = 2
    FATAL = 3

    def __str__(self):
        return self.name

    def __ge__(self, other):
        if self.__class__ is other.__class__:
            return self.value >= other.value
        return NotImplemented

    def __gt__(self, other):
        if self.__class__ is other.__class__:
            return self.value > other.value
        return NotImplemented

    def __le__(self, other):
        if self.__class__ is other.__class__:
            return self.value <= other.value
        return NotImplemented

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented


class Lint(object):
    def __init__(self, config={}):
        self.config = config

    def validate(self, resource):
        result = self.validate_resource(resource)
        if result is None:
            return []
        return result

    def validate_resource(self, resource):
        pass

    def create_issue(self, block=0, line=0, **kwargs):
        return Issue(self.severity, u"{} {}".format(self.__class__.__name__, self.message.format(block=block, line=line, **kwargs)))


class BlockwiseLint(Lint):
    def validate_resource(self, resource):
        issues = []
        if 'block' in resource.content:
            for idx, block in enumerate(resource.content.block):
                blockIssues = self.validate_block(idx, block)
                if blockIssues:
                    issues += blockIssues
        else:
            issues += self.validate_block(-1, resource.content)
        return issues

    def validate_block(self, blockIndex, block):
        pass


class LinewiseLint(BlockwiseLint):
    def validate_block(self, blockIndex, block):
        issues = []
        for idx, line in enumerate(block.line):
            lineIssues = self.validate_line(blockIndex, idx, line)
            if lineIssues:
                issues += lineIssues
        return issues

    def validate_line(self, blockIndex, lineIndex, line):
        pass


class Issue(object):
    def __init__(self, severity, message):
        self.severity = severity
        self.message = message

    def __repr__(self):
        return str([str(self.severity), self.message])

    def add_to(self, bucket):
        bucket.append(self)

    def __eq__(self, other):
        return (isinstance(other, self.__class__) and self.__dict__ == other.__dict__)

    def __ne__(self, other):
        return not self.__eq__(other)
