#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from onyx.core.assets import decodeJSON
from onyx.core.assets import getGeolocalisation


def getText() :
	geoloc = getGeolocalisation.get()
	result = decodeJSON.decodeURL("http://api.openweathermap.org/data/2.5/forecast/daily?lat=" + str(geoloc["lat"]) + "&lon=" + str(geoloc["lon"]) + "&cnt=14&mode=json&units=metric&lang=fr&appid=184b6f0b48a04263c59b93aee56c4d69")
	return "Il fait " + str(round(result["list"][0]["temp"]["day"])) + " degrès à " + str(result["city"]["name"]) + " !"

def get():
	geoloc = getGeolocalisation.get()
	result = decodeJSON.decodeURL("http://api.openweathermap.org/data/2.5/forecast/daily?lat=" + str(geoloc["lat"]) + "&lon=" + str(geoloc["lon"]) + "&cnt=14&mode=json&units=metric&lang=fr&appid=184b6f0b48a04263c59b93aee56c4d69")
	return result


def getCity():
	geoloc = getGeolocalisation.get()
	return str(geoloc["city"])


def getLat():
	geoloc = getGeolocalisation.get()
	return str(geoloc["lat"])

def getLon():
	geoloc = getGeolocalisation.get()
	return str(geoloc["lon"])

