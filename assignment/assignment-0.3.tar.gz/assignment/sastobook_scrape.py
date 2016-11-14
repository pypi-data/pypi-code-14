import scrapy
#scrapy framework for web crawling 	

class SastoBookSpider(scrapy.Spider):
	'''summary of class here:
	Attributes :
	name = string indicating name of site
	allowed_domains = indicating name of domain used
	start_urls = given the url of the provided book '''
	name = 'sastobook'
	allowed_domains = ['www.sastobook.com']
	start_urls = [
		'http://www.sastobook.com/book/by-the-river-piedra-i-sat-down-and-wept'
	]

	def parse(self, response):
		#a class for parsing product category
		book_name = response.xpath("//div[@class='container main-container']/div[@class='inner_container']/h2/text()").extract()[0]
		#extracts name of the book from the given url using xpath
		book_price = response.xpath("//div[@class='book_sellers']/table/tr[2]/td/div[@class='price_after_discount']/text()").extract()[0].split()[0]
		#extracts price of the book from the given url using xpath
		print '\n\nBook Name : ', book_name
		print 'Book Price : ', book_price, '\n\n'
		f = open('sasto.txt', 'w')
		f.write(book_price)
		#opens a file sasto.txt and writing the extracted price in here
		f.close()
		#closes file
