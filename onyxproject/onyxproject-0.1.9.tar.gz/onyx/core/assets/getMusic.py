#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from onyx.core.config import music

def launch():
	os.system("mocp -S")
	os.system("mocp -a " + music.MUSIC_REPO)
	os.system("mocp -t shuffle")

def play():
	os.system("mocp -p")

def pause():
	os.system("mocp -G")

def stop():
	os.system("mocp -x")

def next():
	os.system("mocp -f")

def previous():
	os.system("mocp -r")

def getMusic(name):
	os.system('mplayer ' + music.MUSIC_REPO  + name)

def getRing(name):
	os.system('mplayer ' + music.RING_REPO  + name)
