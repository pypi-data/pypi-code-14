#!/usr/bin/python
# -*- coding: ascii -*-
"""
\brief      Class which stores a log line, including the text, the colours (both, foreground and background).
\author     imoren2x
\copyright  CC BY-NC-SA 4.0
"""


class LogLine(object):
    """
    """
    string = "string"

    color_fg = "color_fg"
    DEFAULT_FG = "grey"

    color_bg = "color_bg"
    DEFAULT_BG = "black"

    def __init__(self, *args, **kwargs):
        """
        """
        self.__string = kwargs[LogLine.string]
        self.__color_fg = kwargs[LogLine.color_fg]
        self.__color_bg = kwargs[LogLine.color_bg]

    def get_string(self):
        """
        """
        return self.__string

    def get_color_fg(self):
        """
        """
        return self.__color_fg

    def get_color_bg(self):
        """
        """
        return self.__color_bg


if __name__ == "__main__":
    #BLACK, BLUE, GREEN, CYAN, RED, MAGENTA, YELLOW, GREY = range(8)
    logLine = LogLine(string = "hola, caracola", color_fg = "blue", color_bg = "grey")
    logLine.print_color()
