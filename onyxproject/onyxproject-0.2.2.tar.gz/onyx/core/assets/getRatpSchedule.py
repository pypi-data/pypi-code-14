#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import json
from onyx.core.assets import decodeJSON
from bs4 import BeautifulSoup
import urllib


def getMetro(line , station , direction) : 
	html = urllib.urlopen('http://www.ratp.fr/horaires/fr/ratp/metro/prochains_passages/PP/' + station + '/' + line + '/' + direction).read()
	ratp = BeautifulSoup(html)
	jsonCreate = json.dumps({"line" : ratp.findAll('img')[24].get('alt'), "station" : ratp.findAll('span')[21].string,"direction" : ratp.findAll('td')[1].string,"name1": ratp.findAll('td')[1].string , "horaire1": ratp.findAll('td')[2].string , "name2": ratp.findAll('td')[3].string , "horaire2": ratp.findAll('td')[4].string , "name3": ratp.findAll('td')[5].string , "horaire3": ratp.findAll('td')[6].string , "name4": ratp.findAll('td')[7].string , "horaire4": ratp.findAll('td')[8].string})
	result = decodeJSON.decode(jsonCreate)
	return result

def getMetroURL(url) : 
	html = urllib.urlopen(url).read()
	ratp = BeautifulSoup(html)
	jsonCreate = json.dumps({"line" : ratp.findAll('img')[24].get('alt'), "station" : ratp.findAll('span')[21].string,"direction" : ratp.findAll('td')[1].string,"name1": ratp.findAll('td')[1].string , "horaire1": ratp.findAll('td')[2].string , "name2": ratp.findAll('td')[3].string , "horaire2": ratp.findAll('td')[4].string , "name3": ratp.findAll('td')[5].string , "horaire3": ratp.findAll('td')[6].string , "name4": ratp.findAll('td')[7].string , "horaire4": ratp.findAll('td')[8].string})
	result = decodeJSON.decode(jsonCreate)
	return result

def getRer(line , station , direction) : 
	html = urllib.urlopen('http://www.ratp.fr/horaires/fr/ratp/rer/prochains_passages/' + line + '/' + station + '/' + direction).read()
	ratp = BeautifulSoup(html)
	jsonCreate = json.dumps({"line" : ratp.findAll('img')[24].get('alt'), "station" : ratp.findAll('span')[21].string,"direction" : ratp.findAll('td')[1].string,"name1": ratp.findAll('td')[1].string , "horaire1": ratp.findAll('td')[2].string , "name2": ratp.findAll('td')[3].string , "horaire2": ratp.findAll('td')[4].string , "name3": ratp.findAll('td')[5].string , "horaire3": ratp.findAll('td')[6].string , "name4": ratp.findAll('td')[7].string , "horaire4": ratp.findAll('td')[8].string})
	result = decodeJSON.decode(jsonCreate)
	return result

def getRerURL(url) : 
	html = urllib.urlopen(url).read()
	ratp = BeautifulSoup(html)
	jsonCreate = json.dumps({"line" : ratp.findAll('img')[24].get('alt'), "station" : ratp.findAll('span')[21].string,"direction" : ratp.findAll('td')[1].string,"name1": ratp.findAll('td')[1].string , "horaire1": ratp.findAll('td')[2].string , "name2": ratp.findAll('td')[3].string , "horaire2": ratp.findAll('td')[4].string , "name3": ratp.findAll('td')[5].string , "horaire3": ratp.findAll('td')[6].string , "name4": ratp.findAll('td')[7].string , "horaire4": ratp.findAll('td')[8].string})
	result = decodeJSON.decode(jsonCreate)
	return result