#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import time


def getHour():
	return time.strftime("%H:%M")

def getDate():
	return time.strftime("%d/%m/%Y")

def getDay():
	return time.strftime("%w")
