import scrapy  
#scrapy framework for web crawling

class AzBookSpider(scrapy.Spider):		
	'''summary of class here:
	Attributes :
	name = string indicating name of site
	allowed_domains = indicating name of domain used
	start_urls = given the url of the provided book '''
	name = 'azbook'
	allowed_domains = ['azbookhouse.com']		
	start_urls = [
		'http://azbookhouse.com/book/details/by-the-river-piedra-i-sat-down-wept-1.html'
	]

	def parse(self, response):
		#defines a class for parsing product category
		book_name = response.xpath("//div[@class='section']/h1/text()").extract()[0]
		#extracts name of the book using xpath
		book_price = response.xpath("//div[@class='section']/div[@class='pro_detail']/strong/text()").extract()[0].split()[1]
		#extracts price using xpath
		print '\n\nBook Name : ', book_name
		print 'Book Price : ', book_price, '\n\n'
		f = open('az.txt', 'w')
		f.write(book_price)
		#opens a file az.txt and writing the extracted book_price in it
		f.close()
		#closes file
