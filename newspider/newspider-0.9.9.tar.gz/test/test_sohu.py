# -*- coding: utf-8 -*-
# import sys
# reload(sys)
# sys.setdefaultencoding("utf-8")

from pyquery import PyQuery as pq
import simplejson as JSON
import re
import time

from newspider.interfaces import *
from newspider.spider import Newspider
from newspider.comm.utils import Utils
# from base.commit import PostSession
# from config import *



'''
微博抓取器
'''

class WeiboFetcher(IntFetcher):

    def __init__(self):
        self.next_page = []

    def fetch_detail_urls(self,html):
        #print "aaaa"

        htmlContent = Utils.conv2utf8(html,'GBK')

        #print "bbb"
        #print html
        tag = u"全部"
        l = []

        #htmlContent = unicode(html,'GBK')
        html = pq(htmlContent)
        array = html(".list14 ul li a")
        i = -1
        for item in array:
            element = pq(item)
            i = i + 1
            if i == 0:
                tag = element.text()
                continue
            if i % 2 == 0:
                continue
            url = element.attr('href')
            # text = element.text()
            l.append((url,{"category":tag}))
        return l

    def start_page(self):
        return [  "http://roll.sohu.com/sports_bak/",#>体育</a></li>
            # "http://roll.sohu.com/yule_bak/",#>娱乐</a></li>
            # "http://roll.sohu.com/it_bak/" ,#IT数码</a></li>
            # "http://roll.sohu.com/auto_bak/",# >汽车</a></li>
            # "http://roll.sohu.com/focus_bak/",#>房产</a></li>
            # "http://roll.sohu.com/women_bak/",#>女性</a></li>
            # "http://roll.sohu.com/fashion_bak/",#>时尚</a></li>
            # #"http://roll.sohu.com/baobao/",# >母婴</a></li>-->
            # "http://roll.sohu.com/health_bak/",# >健康</a></li>
            # "http://roll.sohu.com/cul_bak/",# >文化</a></li>
            # "http://roll.sohu.com/learning_bak/",# >教育</a></li>
            # "http://roll.sohu.com/money_bak/",# >财经</a></li>
            # "http://roll.sohu.com/stock_bak/",# >证券</a></li>
            # "http://roll.sohu.com/games_bak/",# >游戏</a></li>
            # "http://roll.sohu.com/media_bak/",# >媒体</a></li>
            # #"http://roll.sohu.com/city_bak/",# >城市</a></li>
            # #"http://roll.sohu.com/luxury_bak/",# >奢侈品</a></li>
            # #"http://roll.sohu.com/star_bak/",# >评论</a></li>
            # "http://roll.sohu.com/travel/",# >旅游</a></li>
            # #"http://roll.sohu.com/pic/",# >大视野</a></li>
            # #"http://roll.sohu.com/subject_bak/",# >专题</a></li>
          ]

    def next_pages(self):
        time.sleep(1)
        return "http://roll.sohu.com/sports_bak/?t=%d" % int(time.time())

    def getJson(self, temp):
        json_str = temp.replace("FM.view(", "").replace(")</script>", "")
        # print json_str
        json = JSON.loads(json_str)
        return json


class WeiboParser(IntParser):

    def parse(self,tag,htmlContent,extras):
        pass


    def filterUrl(self, url):
        url.replace(" ", "")
        p = re.compile(r"http[s]?://(?:[a-zA-Z]|[0-9]|[-.]|_|/|(?:%[0-9a-fA-F][0-9a-fA-F]))+")
        match = p.findall(url)
        if match:
            print "match %s" % match[0]
            return match[0]
        else:
            return url

    def filterContentText(self, contentText):
        return contentText.strip().replace("\n", '').replace('\t', '')


def test_ctr_c(sp):
    time.sleep(1)
    sp.sigint_handler(None,None)



if __name__ == '__main__':
    sp = Newspider()
    sp.config("USER_AGENT","Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html")
    sp.config('GUARD_INTERVAL', 0)
    sp.config('DEBUG', True)


    sp.add_parser(WeiboParser())
    sp.add_fetcher(WeiboFetcher())

    # import threading
    # t = threading.Thread(target=test_ctr_c, args=(sp,))
    # t.start()

    sp.run()



