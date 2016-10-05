#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    module color for terminal
"""
import os
import sys

import myterm

COLOR_OUT = [myterm.FOREGROUND_DEFAULT, myterm.BACKGROUND_DEFAULT]
COLOR_IN = [myterm.FOREGROUND_PROMPT, myterm.BACKGROUND_PROMPT]
COLOR_ERR = [myterm.FOREGROUND_CRITICAL, myterm.BACKGROUND_CRITICAL]
COLOR_INFO = [myterm.FOREGROUND_INFO, myterm.BACKGROUND_INFO]
COLOR_PROMPT = [myterm.FOREGROUND_PROMPT, myterm.BACKGROUND_PROMPT]

class Unbuffered(object):
    """
        manage buffer
    """
    def __init__(self, stream):
        self.stream = stream
        self.line_buffering = False

    def __getattr__(self, attr):
        """
            attr of buffer
        """
        return getattr(self.stream, attr)

    def write(self, data):
        """
            write in buffer
        """
        pass


class UnbufferedOut(Unbuffered):
    """
        manage buffer out
    """
    def __init__(self, stream):
        Unbuffered.__init__(self, stream)

    def write(self, data):
        myterm.SCREEN.set_color(COLOR_OUT[0], COLOR_OUT[1], self.stream)
        self.stream.write(data)
        self.stream.flush()
        myterm.SCREEN.set_color(
            myterm.FOREGROUND_DEFAULT, myterm.BACKGROUND_DEFAULT, self.stream)
        myterm.SCREEN.clean()

    def prompt(self, data):
        """
            manage of prompt
        """
        myterm.SCREEN.set_color(COLOR_PROMPT[0], COLOR_PROMPT[1],self.stream)
        self.stream.write(data)
        self.stream.flush()
        myterm.SCREEN.set_color(
            myterm.FOREGROUND_DEFAULT, myterm.BACKGROUND_DEFAULT, self.stream)
        myterm.SCREEN.reset()


class UnbufferedErr(Unbuffered):
    """
        manage buffer err
    """
    def __init__(self, stream):
        Unbuffered.__init__(self, stream)

    def write(self, data):
        myterm.SCREEN.set_color(COLOR_ERR[0], COLOR_ERR[1], self.stream)
        self.stream.write(data)
        self.stream.flush()
        myterm.SCREEN.set_color(
            myterm.FOREGROUND_DEFAULT, myterm.BACKGROUND_DEFAULT, self.stream)
        myterm.SCREEN.clean()


class UnbufferedIn(Unbuffered):
    """
        manage buffer in
    """
    def __init__(self, stream):
        Unbuffered.__init__(self, stream)

    def write(self, data):
        myterm.SCREEN.set_color(COLOR_IN[0], COLOR_IN[1], self.stream)
        self.stream.write(data)
        self.stream.flush()
        myterm.SCREEN.set_color(
            myterm.FOREGROUND_DEFAULT, myterm.BACKGROUND_DEFAULT, self.stream)
        myterm.SCREEN.clean()

class UnbufferedInfo(Unbuffered):
    """
        manage buffer info
    """
    def __init__(self, stream):
        Unbuffered.__init__(self, stream)

    def write(self, data):
        myterm.SCREEN.set_color(COLOR_INFO[0], COLOR_INFO[1], self.stream)
        self.stream.write(data)
        self.stream.flush()
        myterm.SCREEN.set_color(
            myterm.FOREGROUND_DEFAULT, myterm.BACKGROUND_DEFAULT, self.stream)
        myterm.SCREEN.clean()



sys.stderr = UnbufferedErr(sys.stderr)
sys.stdin = UnbufferedIn(sys.stdin)
sys.stdinfo = UnbufferedInfo(sys.stdout)
sys.stdout = UnbufferedOut(sys.stdout)
