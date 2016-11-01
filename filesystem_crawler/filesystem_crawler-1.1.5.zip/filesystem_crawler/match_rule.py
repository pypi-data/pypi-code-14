import re


class MatchRule:

    def __init__(self, pattern, polarity=True,
                 dirsOnly=False, filesOnly=False, contentPattern=None):
        self.pattern = re.compile(pattern)
        self.polarity = polarity
        self.dirsOnly = dirsOnly
        self.filesOnly = filesOnly
        self.contentPattern = (
            re.compile(contentPattern) if contentPattern else None)
        if dirsOnly and filesOnly:
            raise Exception("Cannot exclusively include directories and files"
                            " at the same time.")

    def isMatch(self, dirname, isFile):

        if not self.pattern.match(dirname):
            return False, self.polarity

        if isFile:
            if self.dirsOnly:
                return False, self.polarity
            if self.contentPattern and not self.contentMatches(dirname):
                return False, self.polarity

        else:
            if self.filesOnly or self.contentPattern:
                return False, self.polarity

        return True, self.polarity

    def contentMatches(self, dirname):
        try:
            with open(dirname, 'r') as textfile:
                for line in textfile:
                    if self.contentPattern.search(line) is not None:
                        return True
        except:  # not a text file
            pass
        return False
