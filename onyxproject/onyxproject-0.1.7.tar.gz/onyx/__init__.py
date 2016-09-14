#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import platform
import webbrowser
from os.path import exists
import site
import onyx

def run():
	from onyx.core import core
	if exists(str(onyx.__path__[0]) + "/core/install") == True:
		webbrowser.open_new_tab('http://localhost:8080/install')
	else:
		webbrowser.open_new_tab('http://localhost:8080')
	core.run('0.0.0.0', port=8080 , debug=False)


