#!/usr/bin/python
# -*- coding: ascii -*-
"""
\brief      Messages to display from __main__.py function
\author     imoren2x
\copyright  CC BY-NC-SA 4.0
"""

import os
from logs.RotatingFileHandler import DEBUG_DIR

about_msg = "\n" + \
            " Software distributed under Creative Commons licence (CC BY-NC-SA 4.0)\n" + \
            " Ignacio Moreno (imoren2x@users.sourceforge.net).\n" + \
            " Especial thanks to the people who helped me to make this tool."

def how_to_report():
    """
    """
    from os.path import join, dirname, abspath
    directory = dirname(abspath(__file__))
    log_file = join(directory, "logs", "logging.conf")
    debug_files = "debug.log"
    log_directory = os.getcwd()
    debug_folder = join(log_directory, DEBUG_DIR)

    msg = "\n" + \
            "If you have found an issue and you want to report it, send an e-mail to imoren2x@users.sourceforge.net, \n" + \
            " including the input you used, the configuration file, the specific command you executed,\n" + \
            " the response from the command line and the context on how and where it happened.\n\n" + \
            "You can also enable the logging facility in PyLogAnalyser by setting \n" + \
            " the parameter \'-v\' to \'log\' from the command-line \n" + \
            " and then try to reproduce the situation. \n\n" + \
            "You can increase the verbosity level by changing the \'level\' key \n" + \
            "in the configuration file [1], but BE CAREFUL! \n" + \
            "because the log file can be huge in size.\n" + \
            "In that case, attach the \'.log\' files present in the folder [2], \n" + \
            " so you will provide a full internal log which makes easier for us to \n" + \
            " solve the problem.\n\n" + \
            "Thanks for your collaboration.\n" + \
            "\n" + \
            " [1] %s \n" % log_file + \
            " [2] %s \n" % debug_folder

    return msg

def show_demo():
    """
    """
    from os.path import join, dirname, abspath
    directory = dirname(abspath(__file__))
    android_dir = join(directory, "android")
    android_log = "Android_logcat_brief_short.log"
    android_conf = "Android_logcat_brief.conf"

    msg = "\n" + \
          "If you want to watch the advantages of PyLogAnalyser, just go to folder [1] and \n" + \
          " copy the files [2] and [3] into a local folder, open a console window on it,\n" + \
          " and write the following command: \n" + \
          "   $> python -m loganalyser -i %s -c %s --stdout\n\n" % (android_log, android_conf) + \
          "You will experience how the android logcat gets colorized and it's much easier and friendly to follow \n" + \
          " the log.\n" + \
          "\n" + \
          " [1] %s \n" % android_dir + \
          " [2] %s \n" % android_log + \
          " [3] %s \n" % android_conf

    return msg
