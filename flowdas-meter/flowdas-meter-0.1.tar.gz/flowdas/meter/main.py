# coding=utf-8
# Copyright 2016 Flowdas Inc. <prospero@flowdas.com>
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from __future__ import absolute_import

import json
import math
import time

import click

from .engine import run


def build_stat(samples):
    n = len(samples)
    smin = min(samples)
    smax = max(samples)
    ssum = sum(samples)
    ssum2 = 0
    for x in samples:
        ssum2 += x * x
    savg = ssum / n
    sstddev = math.sqrt(max(0, ssum2 / n - savg * savg))
    samples.sort()
    if n % 2:
        smedian = samples[n // 2]
    else:
        smedian = (samples[n // 2] + samples[n // 2 - 1]) / 2
    return 'min %.3f avg %.3f max %.3f median %.3f stddev %.3f (%d samples)' % (
        smin * 1000, savg * 1000, smax * 1000, smedian * 1000, sstddev * 1000, n)


@click.command()
@click.option('--server', default='localhost')
@click.option('--port', default=80)
@click.option('--uri', default='/')
@click.option('--timeout', default=5)
@click.option('--num-call', default=1)
@click.option('--rate', default=20)
@click.option('--num-conn', default=600)
@click.option('--data')
@click.option('--no-progress', is_flag=True)
def main(data, no_progress, **kwargs):
    epoch = time.time()
    if no_progress:
        stat = run(None, **kwargs)
    else:
        with click.progressbar(length=kwargs['num_conn']) as bar:
            stat = run(bar, **kwargs)
    elapsed = time.time() - epoch
    if data is not None:
        with open(data, 'wt') as f:
            json.dump(stat, f)

    # total
    nconn = len(stat['data'])
    nreq = 0
    nres = 0
    for conn in stat['data']:
        nreq += len(conn['requests'])
        for req in conn['requests']:
            if req['status'] > 0:
                nres += 1
    click.echo('Total: connections %d requests %d replies %d test-duration %.3f s' % (nconn, nreq, nres, elapsed))

    # connection
    if nconn > 1:
        conn_rate = (nconn - 1) / (stat['data'][-1]['start'] - stat['data'][0]['start'])
        conn_step = 1000 / conn_rate
    else:
        conn_rate = 0
        conn_step = 0
    maxconn = stat['maxconn']
    samples = []
    for conn in stat['data']:
        if conn['requests'] or conn.get('error') is not None:
            samples.append(conn['latency'])
    click.echo('')
    click.echo(
        'Connection rate: %.1f conn/s (%.1f ms/conn, <=%d concurrent connections)' % (conn_rate, conn_step, maxconn))
    click.echo('Connection time [ms]: %s' % build_stat(samples))
    click.echo('Connection length [replies/conn]: %.2f' % (float(nres) / nconn))

    # request
    if nreq > 1:
        start = stat['data'][0]['start']
        end = start
        for conn in reversed(stat['data']):
            if conn['requests']:
                end = conn['requests'][-1]['start']
                break
        req_rate = (nreq - 1) / (end - start)
        req_step = 1000 / req_rate
    else:
        req_rate = 0
        req_step = 0
    samples = []
    for conn in stat['data']:
        for req in conn['requests']:
            samples.append(req['obytes'])
    req_size = float(sum(samples)) / len(samples)
    click.echo('')
    click.echo('Request rate: %.1f req/s (%.1f ms/req)' % (req_rate, req_step))
    click.echo('Request size [B]: %.1f' % req_size)

    # reply
    status = [0] * 7
    bytes = []
    samples = []
    for conn in stat['data']:
        for req in conn['requests']:
            if req['status'] > 0:
                code = min(6, req['status'] // 100 if req['status'] != 200 else 0)
                status[code] += 1
                samples.append(req['latency2'])
                bytes.append(req['ibytes'])
    res_size = float(sum(bytes)) / len(bytes)
    click.echo('')
    click.echo('Reply time [replies/s]: %s' % build_stat(samples))
    click.echo('Reply size [B]: %.1f' % res_size)
    click.echo('Reply status: 200=%d 1xx=%d 2xx=%d 3xx=%d 4xx=%d 5xx=%d others=%d' % tuple(status))

    # error
    errors = {}
    total = 0
    for conn in stat['data']:
        error = conn.get('error')
        if error is not None:
            if error in errors:
                errors[error] += 1
            else:
                errors[error] = 1
            total += 1
    click.echo('')
    click.echo(('Errors: total=%d' % total) + ''.join([' %s=%d' % (k, errors[k]) for k in sorted(errors.keys())]))


if __name__ == '__main__':
    main()
