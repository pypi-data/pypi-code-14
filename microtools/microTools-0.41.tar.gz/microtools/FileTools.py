import os
import fnmatch
def putContents(name, data):
    """
    saves content to file
    :param name:
    :param data:
    :return:
    """
    f=open(name, "w+")
    f.write(data)
    f.close()


def getContents(name):
    """
    returns file data
    :param name:
    :return:
    """
    f = open(name, "r")
    try:
        return f.read()
    finally:
        f.close()

def getDirContentsRec(dir, pattern=None):
    """
    returns dir content, including subdirectories
    :param dir:
    :type dir: str
    :param pattern: glob style pattern to filter files
    :type pattern: str
    :return: returns list of files
    :rtype: list[str]
    """
    result=[]
    files = os.listdir(dir)
    for file in files:
        fullPath=os.path.join(dir, file)
        if os.path.isdir(fullPath):
            result += getDirContentsRec(fullPath, pattern)
        else:
            if not pattern or fnmatch.fnmatch(fullPath, pattern):
                result.append(fullPath)
    return result


