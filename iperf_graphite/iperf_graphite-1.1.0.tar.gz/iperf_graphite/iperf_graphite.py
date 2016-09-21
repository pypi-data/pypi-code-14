#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    iperf_graphite
    ====
    Runs an iperf3 TCP throughput test in both directions
    :copyright: (c) 2016, Dyn Inc.
    :see LICENSE for more details.
"""

import iperf3
import sys
import time
import os
from socket import socket
import argparse
import re
import yaml

from version import __version__

################################################################################
def no_dots(str):
    ''' Replace dots with underscores '''
    return re.sub(r'\.', '_', str)
    
################################################################################
def run_iperf(args):
    '''
    Runs iperf client TCP test
    Arguments: Dictionary with:
      bind_address: Source address for tests
      server: iperf server
      port: iperf port
      reverse: reverse direction of transfer
    Returns:
      dictionary with 'bps' and 'retransmits' key/values
    '''
    client = iperf3.Client()
    client.bind_address = args['bind_address']
    client.server_hostname = args['server']
    if 'port' in args.keys():
        client.port = args['port']
    else:
        client.port = 5201 # default iperf3 port
    if 'duration' in args.keys():
        client.duration = args['duration']
    else:
        client.duration = 10  # default 10 seconds
    client.zerocopy = True
    if 'reverse' in args.keys() and args['reverse']:
        client.reverse = True
    
    print('Connecting to {0}:{1}'.format(client.server_hostname, client.port))
    r = client.run()
    if r.error:
        print r.error
        return None

    res = {} # Our results dict
    res["bps"] = r.sent_bps
    res["retransmits"] = r.retransmits

    return res
    
################################################################################
def send_to_graphite(args):
    '''
    Send data point and value to graphite server
    Arguments: Dictionary with:
      server: carbon server
      port: carbon port
      data: array of strings
    Returns:
      True
    '''
    
    if 'port' not in args.keys():
        args['port'] = 2003

    sock = socket()
    msg = '\n'.join(args['data']) + '\n'

    try:
        sock.connect((args['server'], args['port']))
    except:
        print 'Could not connect to {0}:{1}'.format(args['server'], args['port'])
        sys.exit(1)
    
    print 'sending {0} to {1}:{2}'.format(msg, args['server'], args['port'])
    sock.sendall(msg)
    sock.close()
    return True

################################################################################
def parse_args():
    """
    Parses command-line arguments
    """
    parser = argparse.ArgumentParser(prog='iperf_graphite', description="send iperf stats to graphite")
    parser.add_argument('-f', dest='config_file', default="config.yml",
                        help="Config file")
    parser.add_argument('-V', '--version', action='version', version='%(prog)s {0}'.format(__version__))

    return parser.parse_args()

################################################################################
def main():
    ''' Main routine '''

    args = parse_args()

    # Parse config file
    with open(args.config_file, 'r') as ymlfile:
        cfg = yaml.load(ymlfile)

    if 'sleep' not in cfg.keys():
        cfg['sleep'] = 0

    for test in cfg['tests']:
        # Build data point string
        hostname = os.uname()[1]
        dp = '{0}.{1}.{2}.tcp'.format(cfg['data_point_prefix'],
                                      no_dots(hostname),
                                      no_dots(test['dst']))

        lines = []
        iperf_args = {
            'bind_address': test['src'],
            'server': test['dst'],
            'port': cfg['iperf_port']
        }

        # Send
        res = run_iperf(iperf_args)
        if res is not None:
            data_point = "{0}_{1}".format(dp, 'tx_bps')
            lines.append('{0} {1} {2}'.format(data_point, res['bps'], int(time.time())))
            data_point = "{0}_{1}".format(dp, 'retransmits')
            lines.append('{0} {1} {2}'.format(data_point, res['retransmits'], int(time.time())))

        # Receive
        iperf_args['reverse'] = True
        res = run_iperf(iperf_args)
        if res is not None:
            data_point = "{0}_{1}".format(dp, 'rx_bps')
            lines.append('{0} {1} {2}'.format(data_point, res['bps'], int(time.time())))
            data_point = "{0}_{1}".format(dp, 'retransmits')
            lines.append('{0} {1} {2}'.format(data_point, res['retransmits'], int(time.time())))

        if lines:
            send_to_graphite({'server': cfg['carbon_server'], 
                              'port': cfg['carbon_port'],
                              'data': lines})

        if cfg['sleep'] > 0:
            time.sleep(cfg['sleep'])

        
if __name__ == '__main__':
    main()
