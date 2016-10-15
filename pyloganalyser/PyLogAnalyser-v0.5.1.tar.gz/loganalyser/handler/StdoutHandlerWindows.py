#!/usr/bin/python
# -*- coding: ascii -*-
"""
\brief      Stdout handler for Windows to be used by StdoutHandler.py
\author     imoren2x
\copyright  CC BY-NC-SA 4.0
"""

import re
from IHandler import IHandler
from ctypes import windll, Structure, c_short, c_ushort, byref

class COORD(Structure):
  #struct in wincon.h
  _fields_ = [("X", c_short), ("Y", c_short)]

class SMALL_RECT(Structure):
  #struct in wincon.h
  _fields_ = [ ("Left", c_short),
               ("Top", c_short),
               ("Right", c_short),
               ("Bottom", c_short)]

class CONSOLE_SCREEN_BUFFER_INFO(Structure):
  #struct in wincon.h
  _fields_ = [ ("dwSize", COORD),
               ("dwCursorPosition", COORD),
               ("wAttributes", c_ushort),
               ("srWindow", SMALL_RECT),
               ("dwMaximumWindowSize", COORD)]

# winbase.h
STD_INPUT_HANDLE  = -10
STD_OUTPUT_HANDLE = -11
STD_ERROR_HANDLE  = -12

# wincon.h
FOREGROUND_BLACK     = 0x0000
FOREGROUND_BLUE      = 0x0001
FOREGROUND_GREEN     = 0x0002
FOREGROUND_CYAN      = 0x0003
FOREGROUND_RED       = 0x0004
FOREGROUND_MAGENTA   = 0x0005
FOREGROUND_YELLOW    = 0x0006
FOREGROUND_GREY      = 0x0007
FOREGROUND_INTENSITY = 0x0008 # foreground color is intensified.

BACKGROUND_BLACK     = 0x0000
BACKGROUND_BLUE      = 0x0010
BACKGROUND_GREEN     = 0x0020
BACKGROUND_CYAN      = 0x0030
BACKGROUND_RED       = 0x0040
BACKGROUND_MAGENTA   = 0x0050
BACKGROUND_YELLOW    = 0x0060
BACKGROUND_GREY      = 0x0070
BACKGROUND_INTENSITY = 0x0080 # background color is intensified.

stdout_handle = windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)

def get_text_attr():
  '''
  Gets the character attributes (colors) of the console screen
  buffer.
  '''
  csbi = CONSOLE_SCREEN_BUFFER_INFO()
  GetConsoleScreenBufferInfo = windll.kernel32.GetConsoleScreenBufferInfo
  GetConsoleScreenBufferInfo(stdout_handle, byref(csbi))
  return csbi.wAttributes

def set_text_attr(color):
  '''
  Sets the character attributes (colors) of the console screen
  buffer.
  Color is a combination of foreground and background color,
  foreground and background intensity.
  '''
  SetConsoleTextAttribute = windll.kernel32.SetConsoleTextAttribute
  SetConsoleTextAttribute(stdout_handle, color)


class StdoutHandlerWindows(IHandler):
    """
    """
    COLORS_str = "BLACK|BLUE|GREEN|CYAN|RED|MAGENTA|YELLOW|GREY"
    DEFAULT_COLORS = get_text_attr()
    FG = "FOREGROUND"
    FG_MASK = 0x000F
    BG = "BACKGROUND"
    BG_MASK = 0x00F0
    
    def __init__(self):
        """
        """
        pass
    
    def open(self):
        """
        """
        pass
    
    def close(self):
        """
        """
        set_text_attr(StdoutHandlerWindows.DEFAULT_COLORS)

    def __set_color_fg(self, color_fg):
        """
        """
        FG = StdoutHandlerWindows.FG
        FG_MASK = StdoutHandlerWindows.FG_MASK
        return self.__set_color(color_fg, FG, FG_MASK)

    def __set_color_bg(self, color_bg):
        """
        """
        BG = StdoutHandlerWindows.BG
        BG_MASK = StdoutHandlerWindows.BG_MASK
        return self.__set_color(color_bg, BG, BG_MASK)
    
    def __set_color(self, color, fg_bg, fg_bg_mask):
        """
        fg_bg_mask = 0x00F0 or 0x000F
        """
        output_color = None

        if color is None:
            #Take color by default
            output_color = StdoutHandlerWindows.DEFAULT_COLORS & fg_bg_mask

        else:
            colors_str = StdoutHandlerWindows.COLORS_str
            colors_regex = re.compile(colors_str)
            if bool(colors_regex.match(color.upper())):
                exec("output_color = " + fg_bg + "_" + color.upper())
            else:
                raise Exception("Color not available. Please, check.")

        return output_color
    
    def append(self, log_line):
        """
        """
        foreground_color = self.__set_color_fg(log_line.get_color_fg())
        background_color = self.__set_color_bg(log_line.get_color_bg())
        string = log_line.get_string()

        set_text_attr(foreground_color | background_color)
        print string,
        set_text_attr(StdoutHandlerWindows.DEFAULT_COLORS)
