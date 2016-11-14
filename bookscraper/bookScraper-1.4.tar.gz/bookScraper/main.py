
import os
from sastobook_scrape import SastoBookSpider
from azbook_scrape import AzBookSpider

class RunnerClass:
    def __init__(self):
        os.system('scrapy crawl sastobook')
        os.system('scrapy crawl azbook')

        sasto = open('sasto.txt', 'r')
        sasto_price = float(sasto.read())

        az = open('az.txt', 'r')
        az_price = float(az.read())

        self.mini = min(sasto_price, az_price)

if __name__ == '__main__':
    print '\n\nMinimum price is: ', RunnerClass().mini, '\n'
