# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os
import re
from droigotools import cmdengine
from droigotools import rootcmd
from droigotools import scmsupport

RULE_PROJECT = re.compile("^[a-zA-Z_]*[a-zA-Z0-9]+([\-_]*[a-zA-Z0-9]+)*[a-zA-Z0-9_]*$")
RULE_LIB = re.compile("^lib[a-zA-Z0-9_]+$")
RULE_PACKAGE = re.compile("^[a-z][a-z0-9]*[A-Z0-9]{0,4}$")
RULE_GOFILE = re.compile("^([a-z_]*[a-z0-9]+([\-_]*[a-z0-9]+)*[a-z0-9_]*)(\.go)?$")

class excCMDGoError(cmdengine.ExcCMDError):
    def __init__(me,msg):
        me.message = msg

def makefile(filename,content,scm,app):
    filepath = os.path.join(app["SOURCEPATH"],app["pack_path"],filename)
    if os.path.exists(filepath):
        raise excCMDGoError("File already exists - %s" % (filepath,))
    fp = open(filepath,"w+")
    fp.write(content)
    fp.close()
    if scm:
        try:
            scm.addFiles(scm.fullPath2SCM(filepath))
        except scmsupport.excSCMError as e:
            app.warn("Failed SCM trace - %s" % (e.message,))

def makegofile(filename,scm,app):
    app["pack_name"] = ( # package name in go-file
            RULE_LIB.match(app["pack_fullname"]) and app["pack_fullname"]) or "main"
    if filename[-3:] != ".go":
        filename = filename + ".go"
    app["pack_path"] = app["pack_path"].replace(os.sep,"/")
    return makefile(filename, str(app.conf["filehead.template"]) % app, scm, app)

# Sub-command: Create project
@rootcmd.rootCmdPath.path("proj","pj")
@cmdengine.pathNew
class ProjCreate(cmdengine.ArgPath):
    _NOTE = "Create new golang project"
    _MAXTARGET = 1

    def init(me):pass

    def finalCmd(me,param):
        if param[0][0] == "/":
            param[0] = param[0][1:]
        if not RULE_PROJECT.match(param[0]):
            raise excCMDGoError("Invalid project name [%s]" % (param[0],))
        me.app["proj_name"] = param[0]
        me.app["pack_fullname"] = me.app["proj_name"]   # package directory name in project
        absPath = os.path.join(me.app["PROJBASE"], me.app["proj_name"])
        me.app["pack_path"] = os.path.relpath(absPath, me.app["SOURCEPATH"])
        if os.path.exists(absPath):
            raise excCMDGoError("Project already exists")
        try:
            os.makedirs(absPath)
        except Exception as e:
            raise excCMDGoError("Can not create project directory - %s" % (e.message,))
        scm = None
        try:
            if me.app["SCMENABLE"]:
                scm = scmsupport.initSCM(me.app["SCMFEATURE"],absPath)
        except scmsupport.excSCMError as e:
            me.app.warn("SCM - %s" % (e.message,))
        makefile("PROJECT", str(me.app.conf["project-readme.template"]) % me.app, scm, me.app)
        makefile("COPY", str(me.app.conf["copyright.template"]) % me.app, scm, me.app)
        makegofile(me.app["proj_name"], scm, me.app)
        return ""

# Base class for create something into a project
class ProjCreateSub(cmdengine.ArgPath):
    _MAXTARGET = 1

    def init(me):pass

    def fillWorkEnv(me,packsplit):
        if not packsplit or packsplit[0]:
            pack_relpath = os.path.relpath(
                    os.path.join(me.app["WORKPATH"],*packsplit), me.app["PROJBASE"])
            if pack_relpath and pack_relpath[0] != ".":
                packsplit = pack_relpath.split(os.sep)
        else:
            packsplit = packsplit[1:]
        if not packsplit:
            raise excCMDGoError("No target specified")
        me.app["proj_name"] = packsplit[0]
        pack_rel = packsplit[1:]
        packname = (pack_rel and pack_rel[-1]) or None
        if not RULE_PROJECT.match(me.app["proj_name"]):
            raise excCMDGoError("Invalid package path, project name [%s] is not avalable" % (
                me.app["proj_name"],))
        packPath = os.path.join(me.app["PROJBASE"],me.app["proj_name"],*pack_rel)
        if not os.path.exists(packPath):
            raise excCMDGoError("Invalid package path [%s]" % (packPath,))
        me.app["pack_fullname"] = packname or me.app["proj_name"]
        me.app["pack_path"] = os.path.relpath(packPath, me.app["SOURCEPATH"])
        scm = None
        if me.app["SCMENABLE"]:
            scm = scmsupport.searchSCM(me.app["SCMFEATURE"],me.app["proj_name"],me.app["PROJBASE"])
            if not scm:
                me.app.warn("SCM is not avalable in project [%s]" % (me.app["proj_name"],))
        return scm

# Sub-command: Create package
@rootcmd.rootCmdPath.path("package","pk")
@cmdengine.pathNew
class ProjCreatePackge(ProjCreateSub):
    _NOTE = "Create new golang package"

    def finalCmd(me,param):
        packpath = os.path.normpath(param[0]).split(os.sep)
        packname = packpath.pop()
        if not packname:
            raise excCMDGoError("No package name specified")
        if not RULE_PACKAGE.match(packname):
            raise excCMDGoError("Invalid package name [%s]" % (packname,))
        scm = me.fillWorkEnv(packpath)
        me.app["pack_fullname"] = packname
        me.app["pack_path"] = os.path.join(me.app["pack_path"],packname)
        try:
            os.makedirs(os.path.join(me.app["SOURCEPATH"],me.app["pack_path"]))
        except Exception as e:
            raise excCMDGoError("Can not create project directory - %s" % (str(e),))
        makefile("PACKAGE", str(me.app.conf["package-note.template"]) % me.app, scm, me.app)
        makegofile(packname, scm, me.app)
        return ""

# Sub-command: Create package
@rootcmd.rootCmdPath.path("mkfile","f")
@cmdengine.pathNew
class ProjCreatePackge(ProjCreateSub):
    _NOTE = "Create new golang source file"

    def finalCmd(me,param):
        packpath = os.path.normpath(param[0]).split(os.sep)
        filename = packpath.pop()
        if not filename:
            raise excCMDGoError("No file name specified")
        if not RULE_GOFILE.match(filename):
            raise excCMDGoError("Invalid file name [%s]" % (filename,))
        scm = me.fillWorkEnv(packpath)
        makegofile(filename, scm, me.app)
        return ""
