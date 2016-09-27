import os, sys, time
import json
from queue import Queue, Empty
from termcolor import cprint
from urllib.parse import urljoin
from functools import wraps
from collections import defaultdict

sys.path.append(os.getenv("Q_PATH"))
from qlib.asyn import Exe, futures
from qlib.net import to
from qlib.graphy import random_choice
from qlib.spide.agents import AGS
from qlib.spide.web import Handler
from qlib.log import LogControl


LogControl.LOG_LEVEL = LogControl.OK
LogControl.LOG_LEVEL |= LogControl.WRN
LogControl.LOG_LEVEL |= LogControl.INFO
LogControl.LOG_LEVEL |= LogControl.FAIL

info = LogControl.info
err = LogControl.err
fail = LogControl.fail
ok = LogControl.ok
wrn = LogControl.wrn


class SqlHandler(Handler):

    def __init__(self, depth=1, *args, **kargs):
        super(SqlHandler, self).__init__(*args, **kargs)
        self.depth = depth
        self.no_depth = 0
        self.sql_filter = Queue()

    def on_start(self, url, parser):
        self.count = 0
        if parser is None:
            return

        for i in parser.xpath("//a[@href!='']"):
            self.ready_link(i.attrib['href'])

        self.run(self.on_detail, limit_wait=self.try_times)

    def on_detail(self, url, parser):
        # LogControl.ok(url)
        # info("parent: ", url, txt_attr=['bold'])
        if parser is None:
            return

        for i in parser.xpath("//a[@href!='']"):
            link = i.attrib['href']
            if self.no_depth < self.depth:
                # info("put", link)
                self.ready_link(link)
                if self.filter(link):
                    ok("find", link)
                    self.sql_filter.put(link)
            else:
                self.dead()

            if link not in self.reach_url:
                ok('  [%d]' % self.count,end='\r')
                sys.stdout.flush()
                self.count += 1
        self.no_depth += 1

class SqlmapApi:
    """
    Class Task(Table):
        task_id: "some hash id"
        url: str,
        status: 'not running'
        finishtime: time

@get("/task/new")  
@get("/task/<taskid>/delete")  
@get("/admin/<taskid>/list")  
@get("/admin/<taskid>/flush")  
@get("/option/<taskid>/list")  
@post("/option/<taskid>/get")  
@post("/option/<taskid>/set")  
@post("/scan/<taskid>/start")  
@get("/scan/<taskid>/stop")  
@get("/scan/<taskid>/kill")  
@get("/scan/<taskid>/status")  
@get("/scan/<taskid>/data")  
@get("/scan/<taskid>/log/<start>/<end>")  
@get("/scan/<taskid>/log")  
@get("/download/<taskid>/<target>/<filename:path>")  
    """

    TAMPER = [
        'apostrophemask',
        'apostrophenullencode',
        'appendnullbyte',
        'base64encode',
        'between',
        'bluecoat',
        'chardoubleencode',
        'charencode'
    ]

    def __init__(self, id=None, db=None, host="127.0.0.1", port="8775", thread_num=2):
        self.host = host
        self.port = port
        self.exe = Exe(thread_num)
        self.db = db
        self.target = 'http://{host}:{port}'.format(host=host, port=port)
        self.test_url = set()
        self.injectable = defaultdict(lambda:None)
        self.id = id
        self.connect = False

        if self.id is None:
            self.create_task()

    def on_result(self, t, v):
        if t == 'new':
            self.id = v['taskid']
            if self.db is not None:
                self.db.insert("Task", ['task_id', 'url', 'status'], self.id, 'None', 'not running')

        elif t == 'data':
            info(v)
            if v['data']:
                if self.db:
                    self.db.update("Task", )
                else:
                    ok(v['data'])
                    self.injectable = True

        elif t == "status":
            info(v[u'status'])
        elif t == 'start':
            info(v['success'])
        elif t == 'set':
            ok('\ninit options')
        elif t == 'kill':
            fail(v)
        elif t == 'stop':
            wrn(v)
        elif t == 'list':
            for k in v['options']:
                ok(k, v['options'][k])
        elif t == 'task':
            info(v)
        elif t == 'log':
            for msg in v['log']:
                info(msg)

    def handle(self, tag, cmd, **kargs):
        return tag, to(urljoin(self.target, cmd), **kargs).json()

    def create_task(self):
        try:
            self.exe.done(self.handle, self.on_result, 'new', 'task/new')
            self.connect = True
        except Exception as e:
            err("check sqlmapapi server in -> ",self.host, self.port)
            self.connect = False

    def delete_task(self):
        self.cmd('task', 'delete')
        self.id = None
        # self.injectable = False
        # self.test_url = None

    def scan_cmd(self, cmd):
        # self.exe.done(self.handle, self.on_result, cmd, 'scan/{id}/{cmd}'.format(id=self.id, cmd=cmd))
        self.cmd('scan', cmd)

    def task_cmd(self, cmd):
        self.cmd('task', cmd)

    def option(self, cmd):
        self.cmd('option', cmd)

    def cmd(self, tag, cmd):
        if self.connect:
            self.exe.done(self.handle, self.on_result, cmd, '{tag}/{id}/{cmd}'.format(tag=tag, id=self.id, cmd=cmd))
        else:
            wrn("not connect")

    def scan(self, url, **options):
        '''
        @url: target url
        @options: {
                    'tamper': True,
                    'smart': True,
                    'delay': 1
                }
        '''
        if 'tamper' in options:
            options['tamper'] = SqlmapApi.TAMPER

        self.test_url.add(url)
        self.injectable[url] = self.id
        if options:
            data = json.dumps(options)
            self.exe.done(
                self.handle,
                self.on_result,
                'set',
                'option/{id}/set'.format(id=self.id),
                data=data,
                method='post',
                headers={'Content-Type': 'application/json'})

        data = json.dumps({'url': url})
        self.exe.done(
            self.handle,
            self.on_result, 
            'start',
            'scan/{id}/start'.format(id=self.id),
            data=data,
            method='post',
            headers={'Content-Type': 'application/json'})

    def status(self):
        self.scan_cmd('status')

    def log(self):
        self.scan_cmd('log')

    def stop(self, id=None):
        self.scan_cmd("stop")










        
