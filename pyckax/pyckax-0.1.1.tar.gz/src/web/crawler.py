'''
'''
from urllib import request
import bs4, sqlite3

class Crawler:
    # +-------------------------------------------------------------------------
    def __init__(self, parser, database='crawler.db'):
        self.parser = parser
        self.database = database
    # +-------------------------------------------------------------------------
    def crawl(self, host):
        page = request.urlopen(host).read()
        soup = bs4.BeautifulSoup(page,self.parser)
        print(soup.title)
    # +-------------------------------------------------------------------------
    def __pick(self, url, path):
        connection = sqlite3.connect(self.database)
        command = '''
        INSERT INTO a (url) SELECT ? WHERE NOT EXISTS
            (SELECT url FROM a WHERE url=?);
        UPDATE a SET count=count+1 WHERE url=?;
        '''
        cursor = connection.cursor()
        cursor.execute(command,(url,url,url))
    # +-------------------------------------------------------------------------
    def __save(self, url, page):
        pass
