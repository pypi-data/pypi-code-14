
import os
#to run the spider within this  except running it manually

class RunnerClass:
	#constructor for class RunnerClass
	
    def __init__(self):
	os.system('scrapy runspider sastobook_scrape.py')
        os.system('scrapy runspider azbook_scrape.py')

        sasto = open('sasto.txt', 'r')
        sasto_price = float(sasto.read())

        az = open('az.txt', 'r')
        az_price = float(az.read())

        self.mini = min(sasto_price, az_price)
        #calculates minimal price]
        print '\n\nMinimum price is: ', self.mini 
	
	
	
if __name__ == "__main__":
		RunnerClass()
        #runs the class
