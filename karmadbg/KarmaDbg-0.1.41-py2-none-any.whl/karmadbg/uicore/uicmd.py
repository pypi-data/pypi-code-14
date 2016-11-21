
import shlex
import string

def registerUiCommand(name, desc, fn):
    uicmdLst[name] = (name, fn, desc)

def getUiCommand(name):

    cmd = uicmdLst.get(name)
    if cmd:
        return cmd[1]
    return None

def runUiCommand(cmdLine):

    try:

        if not cmdLine:
            return False

        shl = shlex.shlex(cmdLine, posix=True)
        shl.escape = []
        shl.wordchars = string.digits + string.ascii_letters + r"!#$%&()*+,-./:;<=>?@[\]^_`{|}~"
        vars =list(shl)

        if  vars[0][0] != '.':
            return False

        uicmd = getUiCommand( vars[0][1:] )
        if not uicmd:
            return False

        vars = vars[1:]

        ret = uicmd(*vars)

    except:
        print "UI command exception!!!"

    return True

uicmdLst = {}

