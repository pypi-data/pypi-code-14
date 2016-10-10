#!/usr/bin/env python3
import json
import re
import sys
import argparse
import scrapy
from scrapy.crawler import CrawlerProcess
from easyscrape.easy_spider import easy_spider

def start_crawler(settings_obj):
	process = CrawlerProcess({
		'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; WINDOWS NT 5.1'
	})

	# Load spider settings
	easy_spider.load_settings(easy_spider, settings_obj)

	# Start crawling
	process.crawl(easy_spider)
	process.start()

# Return default settings for spider
def get_default_settings_obj():
	settings_obj = {}
	settings_obj["save_html_to_directory"] = False
	settings_obj["save_data_to_csv"] = False
	settings_obj["allowed_domains"] = []
	settings_obj["start_urls"] = []
	settings_obj["csv_output_file"] = "scrape_data.csv"
	settings_obj["html_directory_name"] = "HTMLFiles"
	settings_obj["save_file_regex"] = None
	settings_obj["remove_url_query"] = False
	settings_obj["allow_page_regex"] = None
	settings_obj["deny_page_regex"] = None
	settings_obj["randomize_download_delay"] = 0
	settings_obj["download_delay"] = 0
	settings_obj["depth_priority"] = 1
	settings_obj["data_extract_path"] = None
	return settings_obj

# Download argument
def download(args):
	settings_obj = get_default_settings_obj()
	settings_obj["save_html_to_directory"] = True
	settings_obj["start_urls"] = [args.url]
	settings_obj["allowed_domains"] = [re.match('https?://([^/]+)', args.url).group(1)]
	settings_obj["html_directory_name"] = "HTMLFiles"
	settings_obj["save_file_regex"] = "https?://(.*)"
	start_crawler(settings_obj)

def add_default_settings(settings_obj):
	temp_settings_obj = get_default_settings_obj()

	for key, value in settings_obj.items():
		temp_settings_obj[key] = value

	return temp_settings_obj

# Run argument
def run(args):
	settings_obj = None

	# Read dictionary from json file
	try:
		with open(args.settings, 'r') as jFile:
			settings_obj = json.load(jFile)
	except FileNotFoundError as ex:
		print("SETTINGS FILE NOT FOUND")
		sys.exit(-1)
	except ValueError as ex:
		print("SETTINGS FILE CORRUPTED OR INVALID JSON FORMAT")
		sys.exit(-1)

	# Modify settings
	settings_obj = add_default_settings(settings_obj)

	start_crawler(settings_obj)

def scrape(args):
	settings_obj = get_default_settings_obj()

	settings_obj["save_data_to_csv"] = True
	settings_obj["start_urls"] = [args.url]
	settings_obj["allowed_domains"] = [re.match('https?://(.*)', args.url).group(1)]
	settings_obj["csv_output_file"] = "scrape_data.csv"

	# Read xpath from json file
	try:
		with open(args.xpaths, 'r') as jFile:
			settings_obj["data_extract_path"] = json.load(jFile)
	except FileNotFoundError as ex:
		print("XPATHS FILE NOT FOUND")
		sys.exit(-1)
	except ValueError as ex:
		print("XPATHS FILE CORRUPTED OR INVALID JSON FORMAT")
		sys.exit(-1)
	
	start_crawler(settings_obj)

def main():
	# Parser
	parser = argparse.ArgumentParser(prog='easyscrape', description='Download or scrape the given url, see documentation for more info.')
	subparsers = parser.add_subparsers(title='command', dest='cmd', description='Command for easyscrape, choose from download, run or scrape')
	subparsers.required = True

	download_parser = subparsers.add_parser('download', help='Download all the html files and save it in a directory')
	download_parser.add_argument('url', help='Start crawling from this url')
	download_parser.set_defaults(func=download)

	run_parser = subparsers.add_parser('run', help='Run the scraper using the settings file')
	run_parser.add_argument('settings', help='Settings to be loaded')
	run_parser.set_defaults(func=run)

	scrape_parser = subparsers.add_parser('scrape', help='Scrape data using given xpath to a csv file')
	scrape_parser.add_argument('url', help='Start crawling from this url')
	scrape_parser.add_argument('xpaths', help='List of (column,xpaths) object to be crawled')
	scrape_parser.set_defaults(func=scrape)

	# Parse arguments
	args = parser.parse_args()

	args.func(args)

if __name__ == '__main__':
	main()