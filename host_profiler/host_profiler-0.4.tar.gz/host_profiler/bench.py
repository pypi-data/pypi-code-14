# -*- coding: utf-8 -*-

import psutil
from time import sleep
from os import getloadavg
import signal
import sys
from pandas import DataFrame


def handler(signum, frame):
    sys.exit(0)


class Bench(object):

    def __init__(self, folder):

        self.folder = folder

        self.disk_io_read_before = psutil.disk_io_counters().read_bytes
        self.disk_io_write_before = psutil.disk_io_counters().write_bytes
        self.net_io_in_before = psutil.net_io_counters().bytes_recv
        self.net_io_out_before = psutil.net_io_counters().bytes_sent

        self.df = DataFrame({
            'cpu': [],
            'ram': [],
            'disk_write_bytes': [],
            'disk_read_bytes': [],
            'net_bytes_recv': [],
            'net_bytes_sent': [],
            'load_average_one': [],
            'load_average_five': [],
            'load_average_fifteen': [],
        })
        self.run()

    def run(self):
        for sig in [signal.SIGINT, signal.SIGTERM, signal.SIGQUIT]:
            signal.signal(sig, handler)
        try:
            while True:
                tmpdf = DataFrame({
                    'cpu': [psutil.cpu_percent()],
                    'ram': [psutil.virtual_memory().percent],
                    'disk_write_bytes': [psutil.disk_io_counters().write_bytes - self.disk_io_write_before],
                    'disk_read_bytes': [psutil.disk_io_counters().read_bytes - self.disk_io_read_before],
                    'net_bytes_recv': [psutil.net_io_counters().bytes_recv - self.net_io_in_before],
                    'net_bytes_sent': [psutil.net_io_counters().bytes_sent - self.net_io_out_before],
                    'load_average_one': [getloadavg()[0]],
                    'load_average_five': [getloadavg()[1]],
                    'load_average_fifteen': [getloadavg()[2]],
                })

                self.disk_io_read_before = psutil.disk_io_counters().read_bytes
                self.disk_io_write_before = psutil.disk_io_counters().write_bytes
                self.net_io_in_before = psutil.net_io_counters().bytes_recv
                self.net_io_out_before = psutil.net_io_counters().bytes_sent

                self.df = self.df.append(tmpdf)

                sleep(1)

        except (KeyboardInterrupt, SystemExit):
            tmpdf = DataFrame({
                'cpu': [psutil.cpu_percent()],
                'ram': [psutil.virtual_memory().percent],
                'disk_write_bytes': [psutil.disk_io_counters().write_bytes - self.disk_io_write_before],
                'disk_read_bytes': [psutil.disk_io_counters().read_bytes - self.disk_io_read_before],
                'net_bytes_recv': [psutil.net_io_counters().bytes_recv - self.net_io_in_before],
                'net_bytes_sent': [psutil.net_io_counters().bytes_sent - self.net_io_out_before],
                'load_average_one': [getloadavg()[0]],
                'load_average_five': [getloadavg()[1]],
                'load_average_fifteen': [getloadavg()[2]],
            })

            self.disk_io_read_before = psutil.disk_io_counters().read_bytes
            self.disk_io_write_before = psutil.disk_io_counters().write_bytes
            self.net_io_in_before = psutil.net_io_counters().bytes_recv
            self.net_io_out_before = psutil.net_io_counters().bytes_sent

            self.df = self.df.append(tmpdf)

            with open('{0}/dataframe.html'.format(self.folder), 'w') as f:
                f.write(self.df .to_html())
            with open('{0}/dataframe.csv'.format(self.folder), 'w') as f:
                f.write(self.df.to_csv())
            print('results in {0}/dataframe.html and {0}/dataframe.csv'.format(self.folder))
