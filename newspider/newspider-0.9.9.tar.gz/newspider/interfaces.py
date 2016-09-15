# -*- coding: utf-8 -*-


class IntFetcher:

    def fetch_detail_urls(self, content):
        """
        从content中解析二级页的url地址
        :param content: 一级页的html内容
        :return: 返回(list,extras)
        """
        raise Exception("Method fetch_detail_urls not supported yet")

    def start_page(self):
        """
        初始url
        :return: 返回list或者url
        """
        raise Exception("Method net_url not supported yet")

    def next_pages(self):
        """
        从当前一级页中解析next_page的url地址
        :return: list 或者 string
        """
        raise Exception("Method net_url not supported yet")


class IntParser:
    def parse(self,tag, content, url):
        raise Exception("Method parse not supported yet")



