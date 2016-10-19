# coding=utf-8
# Copyright 2016 Flowdas Inc. <prospero@flowdas.com>
#
# This Source Code Form is subject to the terms of the GNU Affero General
# Public License, v. 3.0. If a copy of the AGPL was not distributed with
# this file, You can obtain one at https://www.gnu.org/licenses/agpl-3.0.html.
from __future__ import absolute_import

import json
import math
import os
import resource
import time

import click

from .engine import run


def build_stat(samples, scale=1000):
    n = len(samples)
    smin = min(samples) if n else float('nan')
    smax = max(samples) if n else float('nan')
    ssum = sum(samples)
    ssum2 = 0
    for x in samples:
        ssum2 += x * x
    savg = ssum / n if n else float('nan')
    sstddev = math.sqrt(max(0, ssum2 / n - savg * savg)) if n else 0
    samples.sort()
    if n % 2:
        smedian = samples[n // 2]
    else:
        smedian = (samples[n // 2] + samples[n // 2 - 1]) / 2 if n else float('nan')
    return 'min %.3f avg %.3f max %.3f median %.3f stddev %.3f (%d samples)' % (
        smin * scale, savg * scale, smax * scale, smedian * scale, sstddev * scale, n)


def print_stat(stat):
    # total
    nconn = len(stat['data'])
    nreq = 0
    nres = 0
    for conn in stat['data']:
        nreq += len(conn['requests'])
        for req in conn['requests']:
            if req['status'] > 0:
                nres += 1
    click.echo(
        'Total: connections %d requests %d replies %d test-duration %.3f s' % (nconn, nreq, nres, stat['duration']))

    # clock
    if nconn > 1:
        target_clock = 1.0 / stat['rate']
        samples = []
        rel_samples = []
        timestamp = None
        conns = stat['data']
        for conn in conns:
            if timestamp is not None:
                samples.append(conn['start'] - timestamp)
                rel_samples.append((conn['start'] - timestamp) / target_clock - 1)
            timestamp = conn['start']
        measured_rate = (len(conns) - 1) / (conns[-1]['clock'] - conns[0]['clock'])
        click.echo('')
        click.echo('Rate [conn/s]: measured=%.1f expected=%d error=%.1f' % (
            measured_rate, stat['rate'], measured_rate - stat['rate']))
        click.echo('Clock time [ms]: %s' % build_stat(samples))
        click.echo('Clock error [%%]: %s' % build_stat(rel_samples, scale=100))
        click.echo('Max Clock Skip: %d' % stat['max_skip'])
    else:
        measured_rate = stat['rate']

    # connection
    if nconn > 1:
        conn_rate = (nconn - 1) / (stat['data'][-1]['start'] - stat['data'][0]['start'])
        conn_step = 1000 / conn_rate
    else:
        conn_rate = 0
        conn_step = 0
    max_conn = stat['max_conn']
    samples = []
    for conn in stat['data']:
        if conn['requests'] or conn.get('error') is not None:
            samples.append(conn['latency'])
    click.echo('')
    click.echo('Socket leak: %d open=%d close=%d' % (stat['open'] - stat['close'], stat['open'], stat['close']))
    click.echo(
        'Connection rate: %.1f conn/s (%.1f ms/conn, <=%d concurrent connections)' % (conn_rate, conn_step, max_conn))
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
    req_size = float(sum(samples)) / len(samples) if samples else 0
    click.echo('')
    click.echo('Request rate: %.1f req/s (%.3f ms/req)' % (req_rate, req_step))
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
    res_size = float(sum(bytes)) / len(bytes) if bytes else 0
    click.echo('')
    click.echo('Reply time [ms]: %s' % build_stat(samples))
    click.echo('Reply size [B]: %.1f' % res_size)
    click.echo('Reply status: 200=%d 1xx=%d 2xx=%d 3xx=%d 4xx=%d 5xx=%d others=%d' % tuple(status))

    # throughput
    conns = stat['data']
    EPOCH = conns[0]['clock']
    CUT = EPOCH + len(conns) / measured_rate
    nr = 0
    for conn in conns:
        reqs = conn['requests'][:]
        if reqs and conn.get('error'):
            reqs.pop()
        for req in reqs:
            if req['status'] // 100 not in (2, 3):
                continue
            if req['start'] + req['latency2'] < CUT:
                nr += 1
    throughput = measured_rate * nr / len(conns)
    click.echo('')
    click.echo('Throughput [reqs/s]: %.1f' % throughput)

    # error
    cerrors = {}
    rerrors = {}
    ctotal = 0
    rtotal = 0
    rcount = 0
    for conn in stat['data']:
        error = conn.get('error')
        rcount += len(conn.get('requests'))
        if error is not None:
            if conn.get('requests'):
                errors = rerrors
                rtotal += 1
                rcount -= 1
            else:
                errors = cerrors
                ctotal += 1
            if error in errors:
                errors[error] += 1
            else:
                errors[error] = 1

    click.echo('')
    click.echo('Error rate [%%]: %.1f' % (100 - 100.0 * rcount / stat['num_conn'] / stat['num_call']))
    click.echo(
        ('Connect Errors: total=%d (%.1f%%)' % (ctotal, 100.0 * ctotal / stat['num_conn'])) + ''.join(
            [' %s=%d' % (k, cerrors[k]) for k in sorted(cerrors.keys())]))
    click.echo(
        ('Request Errors: total=%d (%.1f%%)' % (rtotal, 100.0 * rtotal / rcount if rcount else 0)) + ''.join(
            [' %s=%d' % (k, rerrors[k]) for k in sorted(rerrors.keys())]))


class FakeProgressBar:
    def __init__(self, **kwargs):
        pass

    def __enter__(self):
        return None

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


@click.command()
@click.option('--server', default='localhost')
@click.option('--port', default=80)
@click.option('--uri', default='/')
@click.option('--timeout', default=5)
@click.option('--num-call', default=1)
@click.option('--rate', default=20)
@click.option('--num-conn', default=1000)
@click.option('--data')
@click.option('--step', default=20)
@click.option('--range', '_range', default=1)
@click.option('--delay', default=2)
@click.option('--nofile', default=10240)
@click.option('--force', is_flag=True)
@click.option('--no-progress', is_flag=True)
def main(data, step, _range, delay, nofile, force, no_progress, **kwargs):
    limits = list(resource.getrlimit(resource.RLIMIT_NOFILE))
    if limits[1]:
        nofile = min(nofile, limits[1])
    if limits[0] < nofile:
        limits[0] = nofile
        resource.setrlimit(resource.RLIMIT_NOFILE, limits)
    progressbar = FakeProgressBar if no_progress else click.progressbar
    start = kwargs.pop('rate')
    length = 0
    for i in range(_range):
        rate = start + i * step
        length += 1000000 * kwargs['num_conn'] // rate
    with progressbar(length=length) as bar:
        if data is not None:
            dirname = os.path.dirname(data)
            if dirname and not os.path.exists(dirname):
                os.makedirs(dirname)
            name, ext = os.path.splitext(data)
        else:
            name, ext = 'meter', '.json'
        for i in range(_range):
            rate = start + i * step
            filename = '%s-%d%s' % (name, rate, ext)
            if os.path.exists(filename):
                if not force and data is not None:
                    with open(filename) as f:
                        stat = json.load(f)
                    dst_spec = kwargs['server'], kwargs['port'], kwargs['uri'], rate, kwargs['num_conn'], kwargs[
                        'num_call']
                    src_spec = stat['server'], stat['port'], stat['uri'], stat['rate'], stat['num_conn'], stat[
                        'num_call']
                    if dst_spec == src_spec:
                        if bar:
                            bar.update(1000000 * kwargs['num_conn'] // rate)
                        continue
            if _range > 1 and i > 0:
                time.sleep(delay)
            stat = run(bar, rate=rate, **kwargs)
            with open(filename, 'wt') as f:
                json.dump(stat, f)

    if _range == 1:
        print_stat(stat)


if __name__ == '__main__':
    main()
