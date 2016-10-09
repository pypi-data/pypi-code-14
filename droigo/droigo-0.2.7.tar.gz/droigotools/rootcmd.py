# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import re
import sys
import os
import time
from droigotools import defaultconf
from droigotools import cmdengine
from droigotools import scmsupport

# Main instance
class rootInstance(cmdengine.AppInstance):
    RULE_PROJECT = re.compile("^[a-zA-Z_]*[a-zA-Z0-9]+([\-_]*[a-zA-Z0-9]+)*[a-zA-Z0-9_]*$")
    RULE_PACKAGE = re.compile("^[a-z][a-z0-9]*[A-Z]{0,4}$")
    RULE_GOFILE = re.compile("^([a-z_]*[a-z0-9]+([\-_]*[a-z0-9]+)*[a-z0-9_]*)(\.go)?$")
    #Initialize
    def init(me):
        me["HOME"] = os.path.normpath(os.getenv("HOME")) if os.getenv("HOME") \
                else os.path.normpath(os.getenv("USERPROFILE"))
        me["CONFPATH"] = os.path.join(me["HOME"],defaultconf.CONFIG_DIR)
        me["GOPATH"] = os.path.normpath(os.getenv("GOPATH")) if os.getenv("GOPATH") else None
        if not me["GOPATH"]:
            raise cmdengine.ExcCMDError("Golang environ $GOPATH is not specify")
        me["WORKPATH"] = os.path.normpath(os.getcwd())
        me["SOURCEPATH"] = os.path.join(me["GOPATH"],"src")
        me.conf = defaultconf.readAllConfig(me["CONFPATH"])
        me["DOMAINPATH"] = os.path.join(me["SOURCEPATH"], me.conf["config.json"]["domain"])
        me["PROJBASE"] = me["DOMAINPATH"]
        me["SCMFEATURE"] = "scm" in me.conf["config.json"] and me.conf["config.json"]["scm"]
        me["SCMENABLE"] = True
        me["date"] = time.strftime("%Y-%m-%d %H:%m:%S GMT",time.gmtime())
        me["developer"] = me.conf["config.json"]["developer"]
        me["mail"] = me.conf["config.json"]["mail"]

# Root command{{{
#
# Class
@cmdengine.pathNew
class rootCmdPath(cmdengine.ArgPath):
    _NOTE = "Droi standard tool-chain for Golang project"
    def init(me):pass
    def checkOption(me):
        if me.app["SCMENABLE"]:
            if not scmsupport.existsSCM(me.app["SCMFEATURE"]):
                me.app["SCMENABLE"] = False
                me.app.warn("Invalid SCM check - \"%s\" not found" % (me.app["SCMFEATURE"],))

# Options
@rootCmdPath.paramete("-D")
@rootCmdPath.paramete("--without-domain","without Domain path")
def projDisable(param,app):
    app["PROJBASE"] = app["SOURCEPATH"]

@rootCmdPath.paramete("-S")
@rootCmdPath.paramete("--without-scm","without SCM trace")
def scmDisable(param,app):
    app["SCMENABLE"] = False

@rootCmdPath.paramete("-W")
@rootCmdPath.paramete("--ignore-work-path","Lock work directory to $GOPATH/src")
def scmDisable(param,app):
    app["WORKPATH"] = app["SOURCEPATH"]
#}}}

# Sub-command: Help
@rootCmdPath.path("help","h")
@cmdengine.pathNew
class HelpSub(cmdengine.ArgPath):
    _NOTE = "Show help content"
    def init(me):pass
    def finalCmd(me,param):
        me.app.poppath()
        if param and param[0] in me._parent._SUBCMD:
            me.app.path(param[0])
            return me._parent._SUBCMD[param[0]](me.app,[],me._parent).showHelp()
        return me._parent.showHelp()

