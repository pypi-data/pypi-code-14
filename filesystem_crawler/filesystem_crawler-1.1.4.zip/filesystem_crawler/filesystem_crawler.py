import os


class FilesystemCrawler:

    def __init__(self, matchRules, matchCallback=None):
        self.matchRules = matchRules
        self.matchCallback = matchCallback

    def search(self, topdir, ignoreMatchedDirSubtree=True):
        matchedPaths = []
        for dirpath, __, filenames in os.walk(topdir, topdown=True):
            # append directories
            paths = [(dirpath, False)]

            # append files
            for filename in filenames:
                paths.append((os.path.join(dirpath, filename), True))

            for path, isFile in paths:
                isMatch = False
                for matchRule in self.matchRules:
                    matched, polarity = matchRule.isMatch(path, isFile)
                    isMatch = polarity if matched else isMatch

                if isMatch:
                    match = (path, isFile)
                    matchedPaths.append(match)
                    if self.matchCallback:
                        self.matchCallback(match)
                    if not isFile and ignoreMatchedDirSubtree:
                        break

        return matchedPaths
