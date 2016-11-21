
import shlex
import glob
import re
import string
import os
import pykd

def autoComplete(str, namespace):
    res = autoCompleteFilePath(str)
    if res: return res

    res = autoCompletePykd(str, namespace)
    if res: return res

    return None


def autoCompleteFilePath(competeStr):

    try:

        if not competeStr:
            return None

        for secondTime in (False, True):

            try:

                shl = shlex.shlex(competeStr, posix=True)
                shl.escape = []
                shl.wordchars = string.digits + string.ascii_letters + r"!#$%&()*+,-./:;<=>?@[\]^_`{|}~"
                token =list(shl)[-1]
                break

            except ValueError:
                competeStr += "\""

        pathLst = glob.glob(token + "*")
        if len(pathLst) == 0:
            return None

        commonPrefix = os.path.commonprefix(pathLst)[len(token):]

        if commonPrefix and os.path.isdir(token + commonPrefix):
            commonPrefix += "/"

        hintsLst = []
        for path in pathLst:
            if os.path.isfile(path):
                hintsLst.append( ("file", os.path.split(path)[1],) )
            else:
                hintsLst.append( ("dir", os.path.split(path)[1],) )

        return ( "filePath", commonPrefix, hintsLst)

    except:

        return None

def autoCompletePykd(completeStr, namespace):

    try:

        shl = shlex.shlex(completeStr, posix=True)
        shl.escape = []
        shl.quotes = []
        shl.escapedquotes = []
        shl.wordchars = string.digits + string.ascii_letters + r"!#$%&()*+,-./:;<=>?@[\]^_`{|}~'\""
        token =list(shl)[-1]

        m = re.match(r"(.*)\.(\w*)", token)
        if not m:
            return None

        expr = m.group(1)
        attr = m.group(2)

        try:
            thisobject = eval(expr, namespace)
        except Exception:
            return []

        if type(thisobject) == pykd.typedVar or type(thisobject) == pykd.typeInfo:

            fields = [ field for field in dir(thisobject) if field.startswith(attr) ]

            hintsLst = []
            for hint in fields:
                hintsLst.append( ("file", hint) )
    
            commonPrefix = os.path.commonprefix(fields)[len(attr):]

            return ( "filePath", commonPrefix, hintsLst)

        elif type(thisobject) == pykd.module:

            symbols = sorted( (symbol for symbol, _ in  thisobject.enumSymbols(attr + "*") ) )
            symbols = filter( lambda x: not x.startswith(" "), symbols )

            hintsLst = []
            for hint in symbols:
                hintsLst.append( ("file", hint) )

            commonPrefix = os.path.commonprefix(symbols)[len(attr):]

            return ( "filePath", commonPrefix, hintsLst)

    except:
        return None
