# -*- coding: utf-8 -*-
import os
from urlparse import urlparse

from newspider.comm.utils import Utils


class UrlRecorder:
    CACHE_DIR = '.cache'

    def __init__(self,fsync=True):

        if not os.path.exists(UrlRecorder.CACHE_DIR):
            os.makedirs(UrlRecorder.CACHE_DIR)

        self.map_files = {}
        self.map_cache = {}
        self.fsync = fsync

    def record(self,url):
        # 如果命中了,直接返回即可,无需多吃记录
        if self.hit(url): return

        objUrl = urlparse(url)
        if objUrl is None: return

        host = objUrl.hostname

        if self.fsync: #如果不需要持久保存,则不写文件
            cache_file = "%s/%s.lst" % (UrlRecorder.CACHE_DIR, host)

            file = self.map_files.get(cache_file,None)
            if not file or  file.closed :
                file =  open(cache_file,'a')
                self.map_files[cache_file] = file

            file.write("%s\n" % Utils.md5(url))

        # 游湖文件没有那么快刷磁盘,这里需要在缓存里面多刷一次,免得下次过来可能取不到
        tmp = self.map_cache.get(host,[])
        tmp.append(Utils.md5(url))
        self.map_cache[host] = tmp

    def hit(self,url):
        objUrl = urlparse(url)
        if objUrl is None: return

        host = objUrl.hostname
        list = self.map_cache.get(host,None)

        if list is None and self.fsync:
            # 尝试从文件中加载,这里不考虑内存过大的情况
            cache_file = "%s/%s.lst" % (UrlRecorder.CACHE_DIR, host)
            if os.path.exists(cache_file):
                list = map(lambda x: x.strip(),open(cache_file,'r').readlines())
                self.map_cache[host] = list
        # end if

        md5 = Utils.md5(url)
        return True if list is not None and md5 in list else False

    def shutdown(self):
        for file in self.map_files.keys():
            f = self.map_files.get(file)
            if file is not None: f.close()


if __name__ == '__main__':

    url = "http://www.baidu.com/aaaa?kkk=aaa&bbb=sss"
    obj = UrlRecorder()
    # assert  obj.hit(url) == False

    obj.record(url)
    assert obj.hit(url) == True

    url2 = "http://www.baidu.com/aaaa?kkk=测试中文"

    obj.record(url2)
    assert obj.hit(url2) == True


    obj.shutdown()

