
import os
import scrapy

class RunnerClass:
    def __init__(self):
        os.system('scrapy runspider sastobook_scrape.py')
        os.system('scrapy runspider azbook_scrape.py')

        sasto = open('sasto.txt', 'r')
        sasto_price = float(sasto.read())

        az = open('az.txt', 'r')
        az_price = float(az.read())

        self.mini = min(sasto_price, az_price)

if __name__ == '__main__':
    print '\n\nMinimum price is: ', RunnerClass().mini, '\n'
