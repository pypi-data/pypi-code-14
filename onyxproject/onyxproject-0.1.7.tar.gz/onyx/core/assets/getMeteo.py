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

def getDay():
	geoloc = getGeolocalisation.get()
	result = decodeJSON.decodeURL("http://api.openweathermap.org/data/2.5/forecast/daily?lat=" + str(geoloc["lat"]) + "&lon=" + str(geoloc["lon"]) + "&cnt=14&mode=json&units=metric&lang=fr&appid=184b6f0b48a04263c59b93aee56c4d69")
	return str(round(result["list"][0]["temp"]["day"]))

def getCity():
	geoloc = getGeolocalisation.get()
	result = decodeJSON.decodeURL("http://api.openweathermap.org/data/2.5/forecast/daily?lat=" + str(geoloc["lat"]) + "&lon=" + str(geoloc["lon"]) + "&cnt=14&mode=json&units=metric&lang=fr&appid=184b6f0b48a04263c59b93aee56c4d69")
	return str(result["city"]["name"])

def getImg():
	geoloc = getGeolocalisation.get()
	result = decodeJSON.decodeURL("http://api.openweathermap.org/data/2.5/forecast/daily?lat=" + str(geoloc["lat"]) + "&lon=" + str(geoloc["lon"]) + "&cnt=14&mode=json&units=metric&lang=fr&appid=184b6f0b48a04263c59b93aee56c4d69")
	if result["list"][0]["weather"][0]["main"] == 'Rain':
		url = "rain.png" 
	elif result["list"][0]["weather"][0]["main"] == 'Clear':
		url = "clear.png"
	elif result["list"][0]["weather"][0]["main"] == 'Thunderstorm':
		url = "pikacloud.png"
	elif result["list"][0]["weather"][0]["main"] == 'Drizzle':
		url = "rain.png"
	elif result["list"][0]["weather"][0]["main"] == 'Snow':
		url = "snowing.png"
	elif result["list"][0]["weather"][0]["main"] == 'Atmosphere':
		url = "cloud1.png"
	elif result["list"][0]["weather"][0]["main"] == 'Clouds':
		url = "cloud.png"
	elif result["list"][0]["weather"][0]["main"] == 'Extreme':
		url = "windy.png"
	else:
		url = ""
	

	return url

def getLat():
	geoloc = getGeolocalisation.get()
	return str(geoloc["lat"])

def getLon():
	geoloc = getGeolocalisation.get()
	return str(geoloc["lon"])

