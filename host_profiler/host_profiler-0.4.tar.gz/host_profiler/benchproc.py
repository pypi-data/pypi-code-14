# -*- coding: utf-8 -*-

import psutil
import signal
import sys
from pandas import DataFrame
from os import popen
from threading import Thread, Event
from time import sleep
from subprocess import check_output


def handler(signim, frame):
    print('lel')
    sys.exit(0)


def benchproc(folder, process):
    for sig in [signal.SIGINT, signal.SIGTERM, signal.SIGQUIT]:
        signal.signal(sig, handler)

    pids = get_pid(process)
    if len(pids) == 0:
        print('no process named: {0}\n'.format(process))
        sys.exit(1)
    bench_instances = []

    try:
#        for pid in pids:
#            bench_instances.append(BenchProc(int(pid)))
#        for i in bench_instances:
#            i.setDaemon(True)
#            i.start()
        t = Thread(target=test)
        tt = Thread(target=testtest)
        t.setDaemon(False)
        tt.setDaemon(True)
        tt.start()
        t.start()

    except (KeyboardInterrupt, SystemExit):
        for k, instance in enumerate(bench_instances):
            print('a')
            instance.stop()
            df = instance.get_df()
            print(df)
            instance.join()
            print('b')
            with open('{0}/dataframe_proc_{1}.html'.format(folder, k), 'w') as f:
                f.write(df.to_html())
            with open('{0}/dataframe_proc_{1}.csv'.format(folder, k), 'w') as f:
                f.write(df.to_csv())



def test():
    while True:
        print('lolilol')
        sleep(1)

def testtest():
    while True:
        print('lulalul')
        sleep(1)

def get_pid(process):
    return map(int,check_output(["pidof", process]).split())


class BenchProc(Thread):

    def __init__(self, pid, *args, **kwargs):
        super(BenchProc, self).__init__(*args, **kwargs)
        self.proc = psutil.Process(pid)
        self.event = Event()
        self.df = DataFrame({
            'cpu': [],
            'ram': [],
        })

    def run(self):

        self.event.set()
        while self.event.is_set():
            try:
                tmpdf = DataFrame({
                    'cpu': [self.proc.cpu_percent()],
                    'ram': [self.proc.memory_percent()]
                })
                self.df = self.df.append(tmpdf)
                print(self.df)
                sleep(1)
            except KeyboardInterrupt:
                print('lel')

    def stop(self):
        self.event.clear()
