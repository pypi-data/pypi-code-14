# -*- coding: utf-8 -*-

from psutil import Process
from time import sleep
import signal
import sys
from pandas import DataFrame
from os import popen


def handler(signim, frame):
    sys.exit(0)

def benchproc(folder, process):
    for sig in [signal.SIGINT, signal.SIGTERM, signal.SIGQUIT]:
        signal.signal(sig, handler)

    pid = get_pid(process)
    proc = Process(pid)

    df = Dataframe({
        'cp': [],
        'ram': [],
        'disk_write_bytes': [],
        'disk_read_bytes': [],
        'net_bytes_recv': [],
        'net_bytes_sent': []
    })

    try:
        pass
    except (KeyboardInterrupt, SystemExit):
        #one more put in the dataframe needed 
        with open('{0}/dataframe.html'.format(folder), 'w') as f:
            f.write(df .to_html())
        with open('{0}/dataframe.csv'.format(folder), 'w') as f:
            f.write(df.to_csv())


def get_pid(process):
    lines = popen('ps aux').readlines()
    ret_list = []

    for i in lines:
        if process in i:
            ret_list.append(i.split(' ')[1])
    while '' in ret_list:
        ret_list.remove('')
    return ret_list



if __name__ == '__main__':
    print(get_pid('terminology'))

