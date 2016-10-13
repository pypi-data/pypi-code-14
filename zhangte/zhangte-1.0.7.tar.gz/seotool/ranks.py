#coding:utf8
import pandas as pd
import zhangte
from zhangte import *

class RankDf():

    def __init__(self,**kwargs):
        self.export = "排名监控.xls"    #初始化是这个

        self.T = False

    #批量查收录
    def get_index(self,df,i):
        #查收录
        index = df['收录'][i]
        #针对未收录页面进行更新,也要筛选!
        if index < 1:
            #查收录,如果今天没查过就查一下
            if df.日期[i] != str(zhangte.Base().today(0)):
                index =  zhangte.Baidu().index(self.url)
            #如有收录,就更新一下
            if index > 0:
                df['收录'][i] = index
        return df

    #批量查排名! -  电脑端
    @print_state("开始查询 排名 ")
    def get_rank(self,df,i,zd="pc"):
        #最后查询日期 对比看看是不是今天!如果不是,就查询!
        if df.日期[i] != str(zhangte.Base().today(0)):
            #如果是首页,简单查
            if df["类型"][i] == "首页":
                if zd == "pc":
                    rank = zhangte.Baidu().rank(self.kw,self.url,self.T)[0]
                else:
                    rank = zhangte.Baidu().rank(self.kw,self.url,zd="m")[0]

            #如果是内页或是文章页面,复杂查
            else:
                if zd == "pc":
                    rank = zhangte.Baidu().rank(self.kw,self.url,T=True)[0]
                else:
                    rank = zhangte.Baidu().rank(self.kw,self.url,zd="m")[0]

            print (self.kw,rank,self.url)

            #如果有排名就更新
            if rank > 0:
                if zd == "pc":
                    df['排名'][i] = rank
                else:
                    df['手机排名'][i]= rank
            else:
                if zd=="pc":
                    df['排名'][i] = 200
                else:
                    df['手机排名'][i] = 200
        return df


    #读取配置文件 然后批量查询排名,更新  在导出
    def RanksDf(self):
        self.df = pd.read_excel(self.export)
        #查询首页排名
        for i in self.df.index:
            #每查询一次,就重新导入
            df = pd.read_excel(self.export)
            df.排名.astype("int")  #数据类型转换一下

            self.kw = df['关键词'][i]
            self.url = df['域名'][i]

            df = self.get_rank(df,i)    #获取排名 - pc
            df = self.get_rank(df,i,zd ="m")  #获取手机排名
            #获取手机排名
            df = self.get_index(df,i)        #获取收录


            #查询完再导出
            df.日期[i] = str(zhangte.Base().today(0))
            df.to_excel(self.export,index=False)

#集成mysql这个类
class importMysql(zhangte.Mysql):
    def __init__(self,*args,**kwargs):
        super(importMysql,self).__init__(*args,**kwargs)
        self.data = "排名监控.xls"
        self.table = "seo.百度排名监控"

    @print_state("正在导入导入mysql")
    def importsql(self):
        self.df = pd.read_excel(self.data)
        #如果未导入,就开始导入!
        if self.panduan():
            #把他变量遍历出来就可以了
            self.dfinsertsql(self.df,self.table.split('.')[1])

    #判断有没有插入!?
    def panduan(self):
        df = pd.read_sql("SELECT * FROM {};".format(self.table),self.conn)
        #如果今天存在最后3行里面,说明已经采集过!

        if str(self.today(0)) in list(df['日期'].tail(3)):
            print ("今天已经导入过,不导入了!")
            return False
        else:
            print ("今天还没有导入!开始导入!")
            return True


def main(db,export,T,table="seo.百度排名监控",**kwargs):
    a=RankDf(**kwargs)     #批量查排名
    while True:
        a.T = T
        a.export = export    #重新赋值导出文件
        a.RanksDf()


        #如果最后一条等于"今天",那就停止  这一行判断有问题
        if str(zhangte.Base().today(0)) == a.df.日期.tail(1).values[0]:
            print ("今天已经全部查询完开始导入,开始导入!")
            break
        else:
            print("开始继续查询下一个词")

    #导入到sql
    a = importMysql(db,**kwargs)
    a.table = table     #自定义导入tbale

    #把这2个方法抽象出来 -- 直接写在main里面就可以了

    a.data = export     #这个是合并以后的数据
    a.importsql()





if __name__ == '__main__':
    main(db,**kwargs)

