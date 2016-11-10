#!/usr/bin/env python
# -*- encoding=utf8 -*-

'''
FileName:   trace.py
Author:     Chen Yanfei
@contact:   gzchenyanfei@corp.netease.com
@version:   $Id$

Description:

Changelog:

'''

import sys
import traceback
import threading


def get_frame(t):
    return sys._current_frames().get(t.ident)


def format_thread_stack_trace(t):
    f = get_frame(t)
    if f:
        return ''.join(traceback.format_stack(f))
    else:
        return ''

threading.Thread.get_frame = get_frame
threading.Thread.format_stack_trace = format_thread_stack_trace
