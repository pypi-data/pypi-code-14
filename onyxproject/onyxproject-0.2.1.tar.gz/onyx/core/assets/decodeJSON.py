#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import requests
import json


def decodeURL(url) :
	r = requests.get(url, auth=('user', 'pass'))
	t = r.json()
	return t

def decode(jsonToRead) :
	r = jsonToRead
	reply = json.loads(r)
	return reply
