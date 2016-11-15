
import os

class RunnerClass:
    def __init__(self):
        
        # this_file_path = os.path.dirname(os.path.realpath(__file__))
        # print this_file_path

        sasto_path = '/home/ano/assignmentsptyma' + '/sastobook_scrape.py'
        az_path = '/home/ano/assignmentsptyma' + '/azbook_scrape.py'

        # print sasto_path

        os.system('scrapy runspider ' + sasto_path)
        os.system('scrapy runspider ' + az_path)

        sasto = open('sasto.txt', 'r')
        sasto_price = float(sasto.read())

        az = open('az.txt', 'r')
        az_price = float(az.read())

        self.mini = min(sasto_price, az_price)

if __name__ == '__main__':
    print '\n\nMinimum price is: ', RunnerClass().mini, '\n'