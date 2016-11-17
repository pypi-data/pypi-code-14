#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Simple script for listing all the downstreams and upstreams of a cable modem.

To get the stats of your cable modem at 192.168.100.1, you would type at the command line:
```
modem-stats.py 192.168.100.1
```


Created by phillip on 11/16/2016
"""
import sys

from cable_modem_stats import connect


def main(address):
    modem = connect(address)
    print(modem)
    print("Get all downstreams:")
    for ds in modem.downstreams:
        print(ds)

    print("\r\nGet all upstreams")
    for us in modem.upstreams:
        print(us)


if __name__ == "__main__":
    main(sys.argv[1])
