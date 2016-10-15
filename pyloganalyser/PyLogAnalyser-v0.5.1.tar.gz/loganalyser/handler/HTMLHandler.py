#!/usr/bin/python
# -*- coding: ascii -*-
"""
\brief      HTML handler for obtaining HTML log output
\author     imoren2x
\copyright  CC BY-NC-SA 4.0
"""

import os
import HTMLHandlerStrings


class HTMLHandler(object):
    """
    HTML handler class for obtaining HTML log output.
    """

    DEFAULT_FG = "black"
    DEFAULT_BG = "white"

    def __init__(self, filename):
        """
        """
        self.__ori_filename = filename
        self.__filename = os.path.abspath(filename)
        self.__filedesc = file(self.__filename, 'w')
        self.__prepare_doc()

    def __prepare_doc(self):
        """
        """
        self.__filedesc.write(HTMLHandlerStrings.DOC_VER)
        self.__filedesc.write("\n")
        self.__filedesc.write(HTMLHandlerStrings.DOCTYPE)
        self.__filedesc.write("\n")
        self.__filedesc.write(HTMLHandlerStrings.HTML_MAIN_TAG)
        self.__filedesc.write(HTMLHandlerStrings.set_title())
        self.__filedesc.write(HTMLHandlerStrings.set_head())
        self.__filedesc.write(HTMLHandlerStrings.BODY_HEAD)

    def open(self):
        """
        """
        pass

    def close(self):
        """
        """
        closing_str = HTMLHandlerStrings.HTML_END
        self.__filedesc.write(closing_str)
        self.__filedesc.close()

    def append(self, log_line):
        """
        """
        msg_string = log_line.get_string().strip()
        color_fg = None
        color_bg = None

        #color_fg   = log_line.get_color_fg().lower() if (log_line.get_color_fg() is not None) else HTMLHandler.DEFAULT_FG
        if (log_line.get_color_fg() is not None):
            color_fg = log_line.get_color_fg().lower()
        else:
            color_fg = HTMLHandler.DEFAULT_FG

        #color_bg   = log_line.get_color_bg().lower() if (log_line.get_color_bg() is not None) else HTMLHandler.DEFAULT_BG
        if (log_line.get_color_bg() is not None):
            color_bg = log_line.get_color_bg().lower()
        else:
            color_bg = HTMLHandler.DEFAULT_FG
        #
        self.__filedesc.write(HTMLHandlerStrings.set_line(msg_string, color_fg, color_bg))
        #Could include raise the exception.
