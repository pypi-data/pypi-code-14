
import os

class RunnerClass:
    def __init__(self):
        os.system('scrapy runspider bookScrape/bookScrape/sastobook_scrape')
        os.system('scrapy runspider bookScrape/bookScrape/azbook_scrape')

        sasto = open('sasto.txt', 'r')
        sasto_price = float(sasto.read())

        az = open('az.txt', 'r')
        az_price = float(az.read())

        self.mini = min(sasto_price, az_price)

if __name__ == '__main__':
    print '\n\nMinimum price is: ', RunnerClass().mini, '\n'
