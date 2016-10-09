# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os
import subprocess

# SCM implament list
__SCM_FEATURE = {}
def scmclass(name):
    def appendSCM(scmcls):
        __SCM_FEATURE[name] = scmcls
        return scmcls
    return appendSCM

# Exceptions
class excSCMError(Exception): pass
class excSCMGitError(excSCMError): pass
class excSCMMercurialError(excSCMError): pass

# Search SCM loop-back to parent
def searchSCM(feature,relative,basepath=None):
    if feature not in __SCM_FEATURE:
        raise excSCMError("unknown feature of SCM")
    scmcls = __SCM_FEATURE[feature]
    if not scmcls.hasSCM():
        raise excSCMError("SCM is not available")
    if basepath:
        abspath = lambda relpath_l: os.path.join(basepath, *relpath_l)
    else:
        abspath = lambda relpath_l: os.path.join(*relpath_l)
    rellist = os.path.normpath(relative).split(os.sep)
    while rellist:
        where = abspath(rellist)
        if scmcls.hasTrace(where):
            return scmcls(where)
        rellist.pop()
    return None

# check SCM exists
def existsSCM(feature):
    if feature not in __SCM_FEATURE:
        return False
    return __SCM_FEATURE[feature].hasSCM()

def initSCM(feature,basepath):
    if feature not in __SCM_FEATURE:
        return None
    return __SCM_FEATURE[feature](basepath,True)

def startSCM(feature,basepath):
     if feature not in __SCM_FEATURE:
         return None
     return __SCM_FEATURE[feature](basepath)

# Abstrict SCM class
class baseSCM(object):
    # Set repository path named "repopath"
    #def __init__(me,where,init = False):
    #   me.repopath = where or os.getcwd()
    # pre-defined method: SCM command available
    @staticmethod
    def hasSCM(): return False
    # pre-defined method: check path is been traced in SCM
    @staticmethod
    def hasTrace(path): return False
    # map fullpath to SCM relative path
    def fullPath2SCM(me, fullpath):
        rpath = os.path.relpath(fullpath, me.repopath)
        if not rpath or rpath[:2] == "..":
            raise excSCMError("Specify path is not a sub-directory of SCM root")
        return rpath
    # pre-defined method: initialize SCM trace in specify path
    def initSCM(me):pass
    # Preprocess interface for add files trace
    def addFiles(me,*filelist,**option):
        if "relativepath" in option:
            relpath = option["relativepath"]
            mkpath = lambda fname: os.path.join(relpath,fname)
        else:
            mkpath = lambda fname: fname
        return me._addFilesImp([mkpath(fone) for fone in filelist])
    # pre-defined method: Implament for add files trace
    def _addFilesImp(me,files):pass

# Git implament {{{
@scmclass("git")
class GitSCM(baseSCM):
    @staticmethod
    def hasSCM():
        try:
            subprocess.call(["git"],stdout=subprocess.PIPE)
        except:
            return False
        return True

    @staticmethod
    def hasTrace(path):
        return os.path.isdir(os.path.join(path,".git"))

    def __init__(me,where,init = False):
        me.repopath = where
        if not me.hasTrace(where):
            if init:
                ok ,msg = me.initSCM()
                if not ok:
                    raise excSCMGitError(msg)
            else:
                raise excSCMGitError("No git repositore found in specify path")

    def callProc(me,*params):
        try:
            callparam = ["git","-C",me.repopath]
            callparam.extend(params)
            proc = subprocess.Popen(callparam,stdout=subprocess.PIPE)
            return proc.wait() == 0, ""
        except Exception as e:
            return False, str(e)

    def initSCM(me):
        return me.callProc("init")
    
    def _addFilesImp(me,files):
        return me.callProc("add",*files)
#}}}

# Mecurial implament{{{
@scmclass("hg")
class MercurialSCM(baseSCM):
    @staticmethod
    def hasSCM():
        try:
            subprocess.call(["hg"],stdout=subprocess.PIPE)
        except:
            return False
        return True

    @staticmethod
    def hasTrace(path):
        return os.path.isdir(os.path.join(path,".hg"))

    def __init__(me,where,init = False):
        me.repopath = where
        if not me.hasTrace(where):
            if init:
                ok,msg = me.initSCM()
                if not ok:
                    raise excSCMMercurialError(msg)
            else:
                raise excSCMMercurialError("No mercurial repositore found in specify path")

    def callProc(me,*params):
        try:
            callparam = ["hg","--cwd",me.repopath]
            callparam.extend(params)
            proc = subprocess.Popen(callparam,stdout=subprocess.PIPE)
            return proc.wait() == 0, proc.stdout.read()
        except Exception as e:
            return False, e.message

    def initSCM(me):
        return me.callProc("init")
    
    def _addFilesImp(me,files):
        return me.callProc("add",*files)
#}}}

