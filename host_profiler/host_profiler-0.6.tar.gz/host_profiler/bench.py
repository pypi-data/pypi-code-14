# -*- coding: utf-8 -*-

import psutil
from time import sleep
from os import getloadavg
import signal
import sys
from pandas import DataFrame


def handler(signum, frame):
    """handler

    intecept kill signal

    :param signum:
    :param frame:
    """
    sys.exit(0)

def bench(folder):
    """bench

    :param folder:
    """
    for sig in [signal.SIGINT, signal.SIGTERM, signal.SIGQUIT]:
        signal.signal(sig, handler)

    disk_io_read_before = psutil.disk_io_counters().read_bytes
    disk_io_write_before = psutil.disk_io_counters().write_bytes
    net_io_in_before = psutil.net_io_counters().bytes_recv
    net_io_out_before = psutil.net_io_counters().bytes_sent

    df = DataFrame({
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

    try:
        while True:

            tmpdf = DataFrame({
                'cpu': [psutil.cpu_percent()],
                'ram': [psutil.virtual_memory().percent],
                'disk_write_bytes': [psutil.disk_io_counters().write_bytes - disk_io_write_before],
                'disk_read_bytes': [psutil.disk_io_counters().read_bytes - disk_io_read_before],
                'net_bytes_recv': [psutil.net_io_counters().bytes_recv - net_io_in_before],
                'net_bytes_sent': [psutil.net_io_counters().bytes_sent - net_io_out_before],
                'load_average_one': [getloadavg()[0]],
                'load_average_five': [getloadavg()[1]],
                'load_average_fifteen': [getloadavg()[2]],
            })

            disk_io_read_before = psutil.disk_io_counters().read_bytes
            disk_io_write_before = psutil.disk_io_counters().write_bytes
            net_io_in_before = psutil.net_io_counters().bytes_recv
            net_io_out_before = psutil.net_io_counters().bytes_sent

            df = df.append(tmpdf)

            sleep(1)

    except (KeyboardInterrupt, SystemExit):
        tmpdf = DataFrame({
            'cpu': [psutil.cpu_percent()],
            'ram': [psutil.virtual_memory().percent],
            'disk_write_bytes': [psutil.disk_io_counters().write_bytes - disk_io_write_before],
            'disk_read_bytes': [psutil.disk_io_counters().read_bytes - disk_io_read_before],
            'net_bytes_recv': [psutil.net_io_counters().bytes_recv - net_io_in_before],
            'net_bytes_sent': [psutil.net_io_counters().bytes_sent - net_io_out_before],
            'load_average_one': [getloadavg()[0]],
            'load_average_five': [getloadavg()[1]],
            'load_average_fifteen': [getloadavg()[2]],
        })

        disk_io_read_before = psutil.disk_io_counters().read_bytes
        disk_io_write_before = psutil.disk_io_counters().write_bytes
        net_io_in_before = psutil.net_io_counters().bytes_recv
        net_io_out_before = psutil.net_io_counters().bytes_sent

        df = df.append(tmpdf)

        with open('{0}/dataframe.html'.format(folder), 'w') as f:
            f.write(df.to_html())
        with open('{0}/dataframe.csv'.format(folder), 'w') as f:
            f.write(df.to_csv())

