#!/usr/bin/python
# -*- coding: ascii -*-
"""
\brief      distutils setup file
\author     imoren2x
\copyright  CC BY-NC-SA 4.0
"""

from distutils.core import setup

files = ["android/*", "handler/*", "logs/*"]

setup(name="PyLogAnalyser",
      version="v0.5.1",
      description="Python LogAnalyser Tool",
      author="Ignacio Moreno",
      author_email="imoren2x@users.sourceforge.net",
      url="http://pyloganalyser.sourceforge.net/",
      license="CC BY-NC-SA v4.0",
      scripts=[ "PyLogAnalyser User Manual.pdf", 
                "extra_logs/Android_logcat_brief_long.log",
                "extra_logs/Android_logcat_threadtime_long.log"],
      package_data = {'loganalyser' : files },
      packages=["loganalyser"])
