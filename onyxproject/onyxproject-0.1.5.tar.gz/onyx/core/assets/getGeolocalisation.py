#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from onyx.core.assets import decodeJSON

def get() :
	result = decodeJSON.decodeURL("http://ip-api.com/json")
	return result
