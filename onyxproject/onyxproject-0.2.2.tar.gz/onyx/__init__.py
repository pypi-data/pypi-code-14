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
	port=80
	if exists(str(onyx.__path__[0]) + "/core/install") == True:
		webbrowser.open_new_tab('http://localhost:' + str(port) + '/install')
	else:
		webbrowser.open_new_tab('http://localhost:' + str(port))
	try:
		core.run('0.0.0.0', port=port , debug=False)
	except:
		core.run('0.0.0.0', port=8080 , debug=False)


