import scrapy

class AzBookSpider(scrapy.Spider):
	name = 'azbook'
	allowed_domains = ['azbookhouse.com']
	start_urls = [
		'http://azbookhouse.com/book/details/by-the-river-piedra-i-sat-down-wept-1.html'
	]

	def parse(self, response):
		book_name = response.xpath("//div[@class='section']/h1/text()").extract()[0]
		book_price = response.xpath("//div[@class='section']/div[@class='pro_detail']/strong/text()").extract()[0].split()[1]
		print '\n\nBook Name : ', book_name
		print 'Book Price : ', book_price, '\n\n'
		f = open('az.txt', 'w')
		f.write(book_price)
		f.close()
