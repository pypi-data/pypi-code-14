#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-10-06 22:58:46
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

def print_lol(the_list, tab_num):
	"""这是注释
	"""
	for each_item in the_list:
		if isinstance(each_item, list):
			print_lol(each_item, tab_num+1)
		else:
			for each_tab in range(tab_num):
				print("\t", end= '')
			print(each_item)
