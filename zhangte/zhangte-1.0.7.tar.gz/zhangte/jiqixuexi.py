#coding:utf8
import numpy
import jieba
import re
from .base import *
import itertools
from pandas import *
import random
import pandas as pd
from jinja2 import Template

class NLP(Base):
    fuhao="，。\n"

    def get_stopwords(self):
        '''获取停用词'''
        return pd.read_csv(
        "StopwordsCN.txt",
        encoding='utf8',
        index_col=False,
        quoting=3,
        sep="\t"
    )


    #余弦值计算函数( 传入2个向量)
    def cosineDist(self,col1, col2):
        return numpy.sum(col1 * col2)/(
            numpy.sqrt(numpy.sum(numpy.power(col1, 2))) *
            numpy.sqrt(numpy.sum(numpy.power(col2, 2)))
        )


    #字符串分割
    def fenge(self,content):
        list1 = re.split(r'[%s\s]\s*' % self.fuhao, content)
        #更改抓取时间
        while '' in list1:
            list1.remove('')
        return list1


    def FenciAndCutStopwords(self,subCorpos):
        #分词且去除停用词
        sub = []
        segments = []
        for j in range(len(subCorpos)):
            segs = jieba.cut(subCorpos[j])
            for seg in segs:
                if len(seg.strip())>1:
                    sub.append(subCorpos[j])    #目标段落 & 目标文章
                    segments.append(seg)        #对应分词
        segmentDF = pd.DataFrame({'sub':sub, 'segment':segments})
        return segmentDF[~segmentDF.segment.isin(self.stopwords.stopword)]


    def summay(self,content):
        #获取停用词
        self.stopwords = self.get_stopwords()

        #把内容进行分割
        subCorpos = [content] + self.fenge(content)


        #分词且去除停用词
        segmentDF = self.FenciAndCutStopwords(subCorpos)

        #按文章进行词频统计
        segStat = segmentDF.groupby(
                    by=["sub", "segment"]
                )["segment"].agg({
                    "计数":numpy.size
                }).reset_index().sort(
                    columns=["计数"],
                    ascending=False
                )

        #进行文本向量计算
        textVector = segStat.pivot_table(
            index='segment',
            columns='sub',
            values='计数',
            fill_value=0
        )

        target = textVector.ix[:, textVector.apply(numpy.sum)==textVector.apply(numpy.sum).max()]
        textVector = textVector.ix[:, textVector.apply(numpy.sum)!=textVector.apply(numpy.sum).max()]

        distance = textVector.apply(lambda col: self.cosineDist(target.ix[:, 0], col))

        tagis = distance.order(ascending=False)[0:1].index
        return tagis[0]


class Data(Base):

    #标题组合
    def zuhe(self,df,cols,DEBUG=False):
        '''
传入 数据框, 以及想要组合的列,就会生成出来,使用方式
Data().zuhe(df,cols = ["时间词","地方词","动词"]),返回一个可迭代的数据 一个字符串
DEBUG,默认是False,不传入,会直接返回指定格式的字符串,如果是True,则返回元组的格式(可以用与处理一些东西).
如果输入任意数字(大于2)则返回字典!
比如 Data().zuhe(df,cols = ["时间词","地方词","动词"],DEBUG=3),   则可以返回一个字典类型的数据
        '''
        b = pd.Series()
        for col in cols:
            x = pd.Series({col:list(df[df[col].notnull()][col])})
            b = b.append(x)
        for x in itertools.product(*(b.values)):
            if DEBUG == False:
                yield ''.join(x)
            elif DEBUG == True:
                yield x
            else:
                yield dict(list(zip(cols,list(x))))


    #根据语料库生成文章
    def Creat_content(self,df,start=13,end=17,field="content"):
        '''
        自动生成语料库文章的代码,先要制作好语料库,才能用这个函数
        df 就是语料库!
        start,end,随机抽取的段落数量
        field,想要抽取哪个字段的内容
        只要把语料库按照格式最好就可以!
        一般用默认的就可以了,这样使用
        Creat_content(df)
        '''
        r = numpy.random.randint(0, len(df),random.randint(start,end))
        list1 = list(df.loc[r, :][field])
        return self.ListToStr(list1).replace("\u3000","&nbsp;")\
                                    .replace("\n","")\
                                    .replace("\t","")\
                                    .replace("\xa0","")\
                                    .replace("\r","")



    #制作语料库
    def get_yuliao(self,df,start=90,end=180,
                   P =r'[<p>|</p>|<br>|</br>]\s*',
                   filename="语料库",
                   mat = "<p>&nbsp;&nbsp;%s</p><br>"):
        '''
        :param df: 传入需要制作语料库的df
        :param start: 最少几个字符?
        :param end: 最多几个字符?
        :param P: 分割的正则 - 可以考虑优化一下直接传入文件
        :param filename: 导出的文件名,默认是语料库!
        :param mat: 格式化标签模板
        :return: 处理好的df
        '''
        yuliao_df = pd.DataFrame()
        for i in df.index:
            new_df = DataFrame({"url":df.url[i],
                                "title":df.title[i],
                                "content":[mat % i for i in re.split(P,df['content'][i]) \
                                           if start<len(i)<end]})
            yuliao_df = concat([yuliao_df,new_df])
        yuliao_df.to_csv("%s.csv" % filename,index=False)
        return yuliao_df


    #传入df,和对应格式的列表,返回组合好的数据
    def get_all_data(self,df,list_all):
        '''
        构建一个list_all,格式如下,list是需要哪些字段
        list_all = [

        {
        "html":标题模板,
        "list":["样品词","项目词"],
        },
        {
        .....
        },

        [

        使用get_all_data(df,list_all)
        (df为模板数据)
        '''
        all_data = []
        for i in list_all:
            html,list1= (i["html"],i["list"])
            all_data+= list(self.get_kws(df[list1],html))
        return all_data


    #针对标准模板的数据生成!
    def get_kws(self,df,html):
        '''
        用于标题是标准模板,比如{{ 地区词 }}{{ 疑问词 }}可以做{{ 项目词 }}
        需要横向拓展,同时又渲染到标题,用法如下:
        然后,get_kws(df[list1],html),这里的df[list1]
        其实是这样:df[["地区词","疑问词","项目词","品牌词"]]
        根据字段筛选出数据,然后这里面就会处理.
        List1的格式:["地区词","疑问词","项目词","品牌词"]
        一般推荐用  get_all_data(df,list_all) 会更加灵活!
        '''
        meats = self.zuhe(df,df.columns,DEBUG=2)
        template = Template(html)
        for meat in meats:
            yield (template.render(meat))


    #批量生成文章
    def inputarticle(self,kws,df,filename):
        '''
        kws:标题列表
        :param df: 语料库
        :param filename:导出的文件夹
        :return: None
        '''
        from .seo import SeoBase
        for kw in kws:
            content = SeoBase().GetYuliaokuArticle(df,kw)
            fl = open("%s/%s.txt" % (filename,kw),"w")
            fl.write(content)
            fl.close()
            print ("成功写入一篇文章:%s"% kw)