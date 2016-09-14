#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

def speak(text):
	os.system('mplayer "http://translate.google.com/translate_tts?tl=fr&client=tw-ob&q=' + text + '"')