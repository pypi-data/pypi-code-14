from HTMLParser import HTMLParser
import urllib
from bs4 import BeautifulSoup
import subprocess
import time
import os

class CricketScore():
	def __init__(self):
		self.base_url = 'http://www.cricbuzz.com/'
		try:
			self.get_match_choice()
		except:
			print "Unable to fetch live matches."

	def get_match_choice(self):
		try:
			base_html_obj = urllib.urlopen(self.base_url)
			base_html_string = base_html_obj.read().decode('utf-8')
			base_parsed_html = BeautifulSoup(base_html_string, 'html.parser')
			class_attr_to_parse = 'cb-col cb-col-25 cb-mtch-blk'
			body = base_parsed_html.body.find_all('div',{'class':class_attr_to_parse})
			live_matches_dict = {}
			count = 1
			for content in body:
				link = content.find_all('a')
				link_title = link[0].attrs['title']
				link_href = link[0].attrs['href']
				match_dict = {"title":link_title,"href":link_href}
				live_matches_dict.update({count:match_dict})
				count+=1
			for key,val in live_matches_dict.iteritems():
				print key,":",val["title"]
			match_num = int(raw_input("Enter the match number for live notifications:  "))
			self.url = self.base_url+live_matches_dict[match_num]["href"]
			try:
				self.start_process(live_matches_dict[match_num]["title"])
			except KeyboardInterrupt:
				print "Quitting..."
		except:
			print "Please enter correct choice"

	def get_score(self):
		html_obj = urllib.urlopen(self.url)
		html_string = html_obj.read().decode('utf-8')
		parsed_html = BeautifulSoup(html_string,'html.parser')
		result =  parsed_html.body.find('div',attrs={'class':'cb-min-bat-rw'}).text
		return result

	def start_process(self, title):
		previous_score = ''
		previous_runs = 0
		previous_wickets = 0
		title = "Cricket Score "+title
		while(True):
			current_score = self.get_score()
			split_list = current_score.split('/')
			current_runs = split_list[0]
			current_wickets = split_list[1].split(" ")[0]
			if previous_score!=current_score:
				print current_score
				previous_score = current_score
				base_dir = os.path.dirname(os.path.abspath(__file__))
				self.image_path = base_dir+"/cricket.png"

				if previous_runs!=current_runs:
					previous_runs = current_runs
					self.image_path = base_dir+"/bat.png"
				if previous_wickets!=current_wickets:
					previous_wickets = current_wickets
					self.image_path = base_dir+"/out.png"

				subprocess.Popen(['notify-send','-i',self.image_path,title,current_score])
				time.sleep(5)

if __name__ == '__main__':
	try:
		CricketScore()
	except:
		print "Sorry, unable to execute..."

