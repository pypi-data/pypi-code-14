import urllib
import json
from mailer import mail
import sys
import urllib2
import xml.etree.ElementTree as et
from bs4 import BeautifulSoup
import bs4
import requests
import time as t
from datetime import *
import traceback
import pdb
import os
import threading
	

def process_response(response_text):
	mail_this = ''
	pagesoup = BeautifulSoup(response_text, "html.parser")	
	section = pagesoup.find("body")
	return section
	# print section
	# print '******this is the body ection*********** '

def load_offline():
	f = open('page.html','r')
	return f.read()

def get_page(page_link):
	try:
		page  = requests.get(page_link)
		articletext = page.text
		return articletext
	except:
		print traceback.print_exc()
		articletext = ''
		return articletext

def track_page():
	with open('config.JSON','r') as f:
	  credentials = json.load(f)

	page_to_monitor = credentials['link_to_monitor']
	to = credentials['send_alert_to']
	interval = credentials['time_interval']
	print 'Page tracking started.....'
	print 'Tracking url: ' + page_to_monitor
	print 'Checking every: ' + str(interval) + ' secs'
	print 'Sending email alerts to: ' + to
	last_page = process_response(get_page(page_to_monitor))


	while 1:
		t.sleep(interval)
		try:
			page_response  = process_response(get_page(page_to_monitor))
			if (last_page != page_response):
				print 'change detected '
				mail(to, 'change is good bitch', 'change deteched at ' + page_to_monitor)
			else:
				print 'no change detected'			 
			last_page = page_response
			
		except :
			exc_type, exc_value, exc_traceback = sys.exc_info()

			error_message = str(exc_type)+' '+str(exc_value)+' '+str(exc_traceback)
			print error_message
			print traceback.print_exc()
			pass

