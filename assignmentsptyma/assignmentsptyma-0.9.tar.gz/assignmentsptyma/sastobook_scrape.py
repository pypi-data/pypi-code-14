import scrapy

class SastoBookSpider(scrapy.Spider):
	name = 'sastobook'
	allowed_domains = ['www.sastobook.com']
	start_urls = [
		'http://www.sastobook.com/book/by-the-river-piedra-i-sat-down-and-wept'
	]

	def parse(self, response):
		book_name = response.xpath("//div[@class='container main-container']/div[@class='inner_container']/h2/text()").extract()[0]
		book_price = response.xpath("//div[@class='book_sellers']/table/tr[2]/td/div[@class='price_after_discount']/text()").extract()[0].split()[0]
		print '\n\nBook Name : ', book_name
		print 'Book Price : ', book_price, '\n\n'
		f = open('sasto.txt', 'w')
		f.write(book_price)
		f.close()

