#!/usr/bin/python
# -*- coding: ascii -*-
"""
\brief      HTML-handler-extra file which provides Strings for HTML-handler
\author     imoren2x
\copyright  CC BY-NC-SA 4.0
"""

### VERSION ###
### CONSTANTS and STRINGS ###
### FUNCTIONS ###

### VERSION ###
VERSION = float(0.5)
###############

### CONSTANTS and STRINGS ###
DOC_VER = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"

DOCTYPE = "<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.1//EN\"\n" \
          "\"http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd\">"

HTML_MAIN_TAG = "<html xmlns=\"http://www.w3.org/1999/xhtml\" xml:lang=\"en\">\n"

INDENT = "    "

TITLE = INDENT + "<title>%s</title>\n"

HTML_HEAD_p = INDENT + "<head>\n" + \
        2* INDENT + "<meta http-equiv=\"Content-Type\" content=\"text/html;charset=utf-8\" />\n" + \
        2* INDENT + "<META NAME=\"description\" CONTENT=\"HTML (Log description)\"></BR>\n" + \
        2* INDENT + "<!-- Style definitions -->\n" + \
        2* INDENT + "%s\n" + \
        INDENT + "</head>\n"

BODY_HEAD = INDENT + "<body BGCOLOR=#F0F0F0 TEXT=#0F0F0F LINK=#00FF00 ALINK=#FF0000 VLINK=#0000FF >\n" + \
        2* INDENT + "<!-- BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE -->\n\n"

LINE_p = 2* INDENT + "<p style=\"background: %s; color: %s\">%s</p>\n"

HTML_END = INDENT + "</body>\n</html>"
#############################

### FUNCTIONS ###
def set_title(title = None):
    """
    """
    main_str = TITLE
    string = None
    
    if title is None:
        string = main_str % "Document title"
    else:
        string = main_str % title

    return string

def set_head(head = None):
    """
    """
    string = None
    if head is None:
        string = HTML_HEAD_p % ""
    else:
        string = HTML_HEAD_p % head

    return string

def set_line(msg_string, color_fg, color_bg):
    """
    """
    html_string = LINE_p % (color_bg, color_fg, msg_string)

    return html_string

#################
