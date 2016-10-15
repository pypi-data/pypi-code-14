#!/usr/bin/python
# -*- coding: ascii -*-
"""
\brief      Stdout handler for Linux to be used by StdoutHandler.py
\author     imoren2x
\copyright  CC BY-NC-SA 4.0
"""

import re
import StringIO
from IHandler import IHandler

class StdoutHandlerLinux(IHandler):
    """
    Stdout handler class for Linux to be used by StdoutHandler.py
    """
    #grey is not a linux color, but included for Windows back-compatibility
    COLORS_str = "BLACK|BLUE|GREEN|CYAN|RED|MAGENTA|YELLOW|WHITE|GREY"
    BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)

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
        pass

    def append(self, log_line):
        '''
        '''
        linebuf = StringIO.StringIO()

        foreground_color = self.__set_color(log_line.get_color_fg())
        background_color = self.__set_color(log_line.get_color_bg())
        string = log_line.get_string()

        format_1 = self.__linux_format(foreground_color, background_color, dim=False)
        format_2 = self.__linux_format(reset=True)

        linebuf.write("%s%s %s" % (format_1, string.rstrip(), format_2))

        line = linebuf.getvalue()
        print line
        #Could include raise the exception.

    def __set_color(self, color):
        """
        """
        #print color
        if color is None:
            return None

        color = color.upper()        
        output_color = None

        colors_str = StdoutHandlerLinux.COLORS_str
        colors_regex = re.compile(colors_str)
        if bool(colors_regex.match(color)):
            #Grey not permitted in Linux,
            #  change it to Windows instead.
            if color == 'GREY':
                color = 'WHITE'

            exec("output_color = StdoutHandlerLinux.%s" % color)
            exec("output_color = int(output_color)")
        else:
            raise Exception("Color not available. Please, check.")

        #print output_color
        return output_color

    def __linux_format(self, fg=None, bg=None, bright=False, bold=False, dim=False, reset=False):
        # manually derived from http://en.wikipedia.org/wiki/ANSI_escape_code#Codes

        codes = list([])
        if reset: 
            codes.append("0")
        else:
            #Foreground
            if fg is not None: 
                codes.append("3%d" % (fg))
            #Background
            if bg is not None:
                if not bright: 
                    codes.append("4%d" % (bg))
                else: 
                    codes.append("10%d" % (bg))
            #Bold, dimmed:
            if bold: 
                codes.append("1")
            elif dim: 
                codes.append("2")
            else: 
                codes.append("22")

        result = "\033[%sm" % (";".join(codes))

        return result
