# -*- coding: utf-8 -*-
# Autogen configure default

from __future__ import unicode_literals

import json
import os

# Basic support {{{

DIR_MASK = 0o755

# Default configure file list
__FILE_LIST = {}
def defaultFile(filename):
    def addFile(fileobj):
        __FILE_LIST[filename] = fileobj
        return fileobj
    return addFile

# Text file prototype
class GeneralTextFile(object):
    DEFAULT = "Default text"
    def __init__(me,initstr=None):
        if initstr:
            me.filestr = initstr
        else:
            me.filestr = me.DEFAULT
    def __str__(me):
        return me.filestr

# JSON config file prototype
class GeneralJSONConf(dict):
    def __init__(me,initjson=None):
        if initjson:
            for k,v in json.loads(initjson).items():
                me[k] = v
        me.default()
    def default(me): pass
    def __str__(me):
        return json.dumps(me,indent=2)

# Try read or renew configure file
def tryReadConfig(filepath,fileclass):
        if os.path.exists(filepath): # read last configure
            fcnt = open(filepath,"r").read()
            finst = fileclass(fcnt)
        else:# renew
            finst = fileclass()
            fp = open(filepath,"wb+")
            fp.write(str(finst).encode("utf-8"))
        return finst

# read one configure file
def readConfig(basepath,filename):
    return tryReadConfig(os.path.join(basepath,filename), __FILE_LIST[filename])

# read all configure file
def readAllConfig(basepath):
    if not os.path.exists(basepath):
        os.makedirs(basepath,DIR_MASK)
    return {fn:tryReadConfig(os.path.join(basepath,fn),fcls) for fn,fcls in __FILE_LIST.items()}
#}}}

# Sub-directory of configure files in user home
CONFIG_DIR = ".DroiGoTools"

# main configure file
@defaultFile("config.json")
class MainConfig(GeneralJSONConf):
    def default(me):
        # spcify SCM, valid type is "git" or "hg" or "none"
        if "scm" not in me: me["scm"] = "git"
        # name or id of developer
        if "developer" not in me: me["developer"] = os.getlogin() or "your name"
        # mail of worker
        if "mail" not in me: me["mail"] = "yourname@mail-domian.com"
        # golang package domain
        if "domain" not in me: me["domain"] = "proj.droi.com"

# golang file template
@defaultFile("filehead.template")
class GoFileHead(GeneralTextFile):
    DEFAULT = '''/* %(pack_path)s
 * Some discription of package
 * ------------------
 * %(developer)s %(date)s
 * %(mail)s
 * Shanghai Droi Co., Ltd. */

package %(pack_name)s

//import package here
import (
    _"fmt"
)

/* >>>>>>>> Begin your code here >>>>>>>>
 *
 * PRIVATE element or PUBLIC element respective write together please.
 * statements use following arrange:
 *
 *  +- TYPE DEFINE
 *  |  +- ENUM CONST
 *  |
 *  +- INTERFACE DEFINE
 *  |
 *  +- GENERAL CONST
 *  |
 *  +- MODULE VARIABLE
 *  |
 *  +- MODULE FUNCTIONS
 *  |
 *  +- TYPE METHODS
 *
 * <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< */
'''

# copyright file template
@defaultFile("copyright.template")
class LicenseFile(GeneralTextFile):
    DEFAULT = '''Shanghai Droi Technology Co., Ltd.
Create at %(date)s

All Right Reserved.
http://www.droi.com
'''

# package note file template
@defaultFile("package-note.template")
class PackageNoteFile(GeneralTextFile):
    DEFAULT = "Note for your package here"

# project readme file template
@defaultFile("project-readme.template")
class ProjectNoteFile(GeneralTextFile):
    DEFAULT = '''PROJECT: %(proj_name)s
summary of your project
------------------------------------
Note for your project here
'''
