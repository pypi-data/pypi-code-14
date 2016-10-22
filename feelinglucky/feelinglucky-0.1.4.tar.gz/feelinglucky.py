import requests
from bs4 import BeautifulSoup

def clean_result(link):
	link = link['href'].split('//')[-1]
	link = link.split('/')
	del link[-1]
	return '/'.join(link)

def feel_lucky(query):
	

	#retrieve google search data
	req = requests.get('https://www.google.com/search', params={'q':query})
	soup = BeautifulSoup(req.text, 'lxml')

	response = soup.find('h3',attrs={'class':'r'})
	first_result = response.select_one('a')

	return clean_result(first_result)
	# return response


print(feel_lucky('reddit'))





