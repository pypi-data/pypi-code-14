# -*- coding: utf-8 -*-
import Queue
import logging
import signal
import time
import traceback

import threadpool
from comm.guarder import Guarder
from comm.urlrecoder import UrlRecorder
from comm.utils import Utils

from newspider.comm.req import Req
from newspider.interfaces import *


class Newspider:
    TASK_DONE_FLAG = "TASK_DONE"
    TASK_SHUTDOWN_FLAG = 'TASK_SHUTDOWN'

    def __init__(self):
        signal.signal(signal.SIGINT, self.sigint_handler)
        self.configuration = {}
        self.init_default_config()
        self.logger = logging.getLogger('Newspider')

        self.fetchers = []
        self.parsers = []
        self.running = True

        self.workers = threadpool.ThreadPool(self.configuration.get('WORKER_NUM', 5))
        self.category_urls = Queue.Queue(maxsize = 100)
        self.details_urls = Queue.Queue(maxsize = 100 )
        # self.fetchers_map = {}

        self.req = Req(self.configuration)
        self.guarder = Guarder(self.configuration)
        self.recorder = UrlRecorder(True)
        self.category_url_record = UrlRecorder(False)

    def init_default_config(self):
        self.configuration['USER_AGENT']= 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.23 Mobile Safari/537.36'

        logger = logging.getLogger('Newspider')
        logger.setLevel(logging.DEBUG)
        hdr = logging.StreamHandler()
        # formatter = logging.Formatter('[%(asctime)s] %(name)s:%(levelname)s: %(message)s')
        # hdr.setFormatter(formatter)
        logger.addHandler(hdr)

    def config(self,key,value):
        """
        配置参数
        :param key: 可用值： USER_AGENT| WORKER_NUM| GUARD_INTERVAL
        :param value:
        :return:
        """
        self.configuration[key] = value


    def run(self):
        #特殊处理一下
        if self.is_debug():
            self.recorder = UrlRecorder(False) #重新生成一个不写文件的记录器,方便调试

        self.running = True
        self.logger.info("Start to run Newspider with %d fetcher(s) and %d parser(s)..." %(len(self.fetchers),len(self.parsers)))

        #第一步,先将start_page丢到队列中
        for fet in self.fetchers:
            if hasattr(fet,'start_page'):
                urls = fet.start_page()
                if type(urls) is list: [self.category_urls.put((fet, url)) for url in urls]
                else:self.category_urls.put((fet, urls))

        reqs = threadpool.makeRequests(self.do_fetch_details_urls, (self.category_urls,))
        [self.workers.putRequest(req) for req in reqs]

        reqs = threadpool.makeRequests(self.do_fetch_details_content, [self.details_urls] * int(self.configuration.get('WORKER_NUM', 5) - 1))
        [self.workers.putRequest(req) for req in reqs]

        self.workers.wait()

    def do_fetch_details_urls(self,queue):
        """
        【注意】只能在一个线程中处理此函数，不能并行
        处理分类页面，并在分类页面里面抽取子页面也next_page
        :param queue:
        :return:
        """
        self.logger.info("Starting worker for fetching details urls in category page...")
        while self.running and not queue.empty():
            """
            处理逻辑：
            2. 检查门卫系统，如果未满足条件，则将url丢到队列尾部，否则继续
            3. 请求html，
            4. 解析details_url列表，并添加到url列表队列
            5. 解析next_page_url，并添加到queue队列尾部
            """
            try:
                data = queue.get()
                fet, url = data
                if fet is None or url is None: continue

                # 门卫系统检查,如果未到时间,则放回队列中继续等待
                if not self.guarder.check(url):
                    self.logger.debug("Guarder check failed, skip this url for this time")
                    self.category_urls.put((fet, url))
                    time.sleep(1)
                    continue

                # 首先拉取html内容
                html = self.req.get(url)
                if html is not None: self.logger.debug("Got html content from %s" % url)

                # 解析当前页面中的所有详情页面url
                if not hasattr(fet, 'fetch_detail_urls'):
                    self.logger.error("Not method name fetch_detail_urls in fetcher %s" % fet.__class__)
                    continue

                try:
                    url_lists = fet.fetch_detail_urls(html)
                except Exception, e:
                    self.logger.error("Error when calling fetcher's fetch_detail_urls(): %s" % e.message)
                    traceback.print_exc()
                    url_lists=[]

                tag = Utils.tag_of_object(fet)
                self.logger.debug("Found %d detail urls for tag %s. " % (len(url_lists), tag))
                for item in url_lists:
                    url,extras = item
                    self.details_urls.put((tag, url, extras))


                # 解析当前页面中所有下一页的url
                if not hasattr(fet, 'next_pages'):
                    self.logger.error("Not method name next_pages in fetcher %s" % fet.__class__)
                    break

                try:
                    next_page_urls = fet.next_pages()
                except Exception, e:
                    traceback.print_exc()
                    self.logger.error("Error when calling fetcher's fetch_detail_urls(): %s" % e.message)

                if type(next_page_urls) is list:
                    self.logger.debug("Found %d url(s) for next page" % len(next_page_urls))
                    for url in next_page_urls:
                        if not self.category_url_record.hit(url):
                            self.category_urls.put((fet, url))
                            self.category_url_record.record(url)
                else:
                    self.logger.debug("Found one url for next page.")
                    if not self.category_url_record.hit(url):
                        self.category_urls.put((fet, next_page_urls))
                        self.category_url_record.record(url)

            except Exception,e:
                self.logger.warn("Error when process one item from queue, skip it")
                traceback.print_exc()
                continue
        self.details_urls.put(Newspider.TASK_DONE_FLAG)
        self.logger.info("Category fetcher exist now")

    def do_fetch_details_content(self, queue):
        """
        消费者线程处理函数。处理details_urls列表中的url，并丢给parsers处理
        :param queue:
        :return:
        """
        while self.running:
            """
            处理逻辑：
            1. 如果遇到中止标记，并且队列为空，则中止此线程；否则将中止标记继续丢给队尾
            2. 检查门卫系统，如果检查不通过，则将data丢到队尾，中止当前过程
            3. 最后再丢给parser处理
            """
            try:
                data = queue.get(True, 2)
                if isinstance(data, basestring) and data == Newspider.TASK_SHUTDOWN_FLAG:
                    self.logger.info("Found shutdown flag from queue")
                    with queue.mutex: queue.queue.clear()
                    queue.put(data)
                    break

                if isinstance(data, basestring) and data == Newspider.TASK_DONE_FLAG:
                    if queue.empty():
                        self.logger.info("Found quit flag from queue.")
                        queue.put(data)
                        break
                    else:
                        queue.put(data)
                        continue

                if type(data) is tuple:
                    tag,url,extras = data
                    if self.recorder.hit(url):
                        self.logger.debug("Url has beed fetched, skip it. %s" % url)
                    else:
                        # 门卫系统检查,如果未到时间,则放回队列中继续等待
                        if not self.guarder.check(url):
                            self.logger.debug("Guarder check failed, skip this url for this time")
                            queue.put((tag, url, extras))
                            time.sleep(1)
                            continue

                        html = self.req.get(url)
                        if html is not None:
                            extras['_url'] = url
                            self.recorder.record(url)  # 继续扒取过的url
                            for p in self.parsers:
                                try:
                                    p.parse(tag, html, extras)
                                except Exception, e:
                                    traceback.print_exc()
                                    self.logger.error("Failed to parse html for url: %s" % url)


            except Exception, e: pass
        self.logger.info("Do_fetch_details_content worker exist now")

    def add_fetcher(self,fet):
        if isinstance(fet,IntFetcher):
            self.fetchers.append(fet)
        else:
            self.logger.warn("object add to fetchers must be subclass of IntFetcher")

    def add_parser(self,parser):
        if isinstance(parser,IntParser):
            self.parsers.append(parser)
        else:
            self.logger.warn("object add to parsers must be subclass of IntParser")

    def sigint_handler(self, signum, frame):
        self.logger.info('Catched interrupt signal, Newspider will exits now!')
        self.running = False
        self.details_urls.put(Newspider.TASK_SHUTDOWN_FLAG)
        #self.workers.dismissedWorkers(self.configuration.get('WORKER_NUM', 5), False)

    def is_debug(self):
        return self.configuration.get('DEBUG',False) is True

    def __del__(self):
        self.workers.dismissedWorkers(self.configuration.get('WORKER_NUM', 5), False)
        self.recorder.shutdown()


