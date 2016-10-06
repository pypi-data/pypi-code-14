#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-10-06 22:58:46
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

def print_lol(the_list, indent=False, level=0):
	"""这是注释
	"""
	for each_item in the_list:
		if isinstance(each_item, list):
			print_lol(each_item, indent, level+1)
		else:
			if indent:
				for each_tab in range(level):
					print("\t", end= '')
			print(each_item)
