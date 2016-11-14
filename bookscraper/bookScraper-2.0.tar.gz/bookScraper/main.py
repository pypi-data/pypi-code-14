
# import 
from scrapy import cmdline

class RunnerClass:
    def __init__(self):
        # os.system('scrapy runspider sastobook_scrape')
        # os.system('scrapy runspider azbook_scrape')

        cmdline.execute('scrapy runspider sastobook_scrape')
        cmdline.execute('scrapy runspider azbook_scrape')

        sasto = open('sasto.txt', 'r')
        sasto_price = float(sasto.read())

        az = open('az.txt', 'r')
        az_price = float(az.read())

        self.mini = min(sasto_price, az_price)
