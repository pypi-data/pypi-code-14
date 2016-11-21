import sys
import pyperclip
import time
import subprocess
import urllib
from bs4 import BeautifulSoup	

class ShowMeaning():
	def __init__(self):
		self.base_url = 'http://google-dictionary.so8848.com/meaning?word='
		self.start_process()

	def get_meaning(self, word):
		self.url = self.base_url+str(word)
		html_obj = urllib.urlopen(self.url)
		html_string = html_obj.read().decode('utf-8')
		bs_obj = BeautifulSoup(html_string,"html.parser")
		if bs_obj:
			content = bs_obj.find_all('li')
			result = content[4].contents[0]
			return str(result)
		else:
			return ''

	def start_process(self):
		print "Just COPY any word to find its meaning (make sure you are connected to the internet). Your search history will be saved in home/user/Desktop/vocabulary.txt."
		try:
			last_text = pyperclip.paste()
		except:
			print "install xclip using command 'sudo apt-get install xclip'"
		base_dir = "/home/user/Desktop/vocabulary.txt"
		while(True):
			current_text = str(pyperclip.paste())
			if current_text and (str.isalpha(current_text) and current_text!=last_text):
				try:
					meaning = self.get_meaning(current_text)
					result = current_text+" = "+meaning
					subprocess.Popen(['notify-send',"QuickDictionary", result])
					print "Found %s..." %current_text
					file = open(base_dir, "a")
					msg = "\n"+current_text+" : "+meaning
					file.write(msg)
					file.close()
				except Exception as e:
					print e.message
					print "Error getting meaning"
					pass
			last_text = current_text
			
if __name__=="__main__":
	ShowMeaning()