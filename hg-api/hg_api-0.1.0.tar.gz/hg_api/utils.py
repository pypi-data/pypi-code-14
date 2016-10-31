#!/usr/bin/env python
#coding:utf-8
"""
  Author:  dog - <yafeile@sohu.com>
  Purpose: 
  Created: 2016年10月31日
"""

from mercurial.ui import ui as uimod
from mercurial.hg import repository

__all__ = ['ui','output','get_repo']

def _setup_ui():
    return uimod()

ui = _setup_ui()

def output(func):
    def _write(*arg,**kw):
        ui.pushbuffer()
        func(*arg,**kw)
        result = ui.popbuffer()
        return result
    return _write

def get_repo(ui,path):
    return repository(ui, path)