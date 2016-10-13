#coding:utf8
from zhangte.seo import *
from zhangte.base import *
from pandas import DataFrame
import sys
class Score():
    def __init__(self):
        if '--help' in sys.argv:
                print ('''python rank_score.py [keywords_file]
        keywords_file里面每行包含一个关键词，或者是关键词与搜索量（制表符分隔）
        如果仅有关键词数据，则默认各关键词的搜索量都是100
        ''')
                quit()

        self.keywords_file = sys.argv[1]

        d = dict_plus()
        for i, line in enumerate(open(self.keywords_file), 1):
            try:
                kw, s = line.rstrip().split('\t')	#关键词,搜索量
                s = int(s)
            except:
                kw, s = line.rstrip(), 100			#默认关键词的搜索量
            print (i, kw) 							#打印出徐浩和关键词
            urls = Baidu().baidu_serp_urls(kw,rn=10)
            for pos, url in enumerate(urls[:10], 1):	#获取前10的排名
                d.add(Baidu().root_domain(url), Baidu().RANK_SCORE[pos - 1])	#计算前10名排名的分值[给每个排名一个分值],他用升级的字典,其实也可以用pandas
                #这一步主要是进行累加
        print ()
        self.d = d.sort(d)
        print (self.d)

        #生成报告


    #传入df 批量更新标题
    def get_title(self,df):
        pass



    def to_excel(self,name):
        self.d.name = "得分"
        self.d.index.name = "域名"
        DataFrame(self.d).to_excel(name)

