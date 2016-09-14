# -*- coding: utf-8 -*-
# <carbontube - distributed pipeline framework>
#
# Copyright (C) <2016>  Gabriel Falcão <gabriel@nacaolivre.org>
# (C) Author: Gabriel Falcão <gabriel@nacaolivre.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from __future__ import unicode_literals

import zmq
import imp
import logging
import inspect
import argparse

from datetime import datetime
from zmq.devices import Device
from carbontube.util import sanitize_name
from carbontube.servers import Phase
from carbontube.servers import Pipeline
from carbontube.console.base import get_sub_parser_argv
from carbontube.console.base import bootstrap_conf_with_gevent


DEFAULT_CONCURRENCY = 32


def execute_command_run_pipeline():
    """executes an instance of the pipeline manager server.

    :param ``--sub-bind``: address where the server will listen to announcements from Phases

    ::

      $ carbontube pipeline \\
          --sub-bind=tcp://0.0.0.0:6000 \\
          --job-pull-bind=tcp://0.0.0.0:5050

    """

    parser = argparse.ArgumentParser(
        prog='carbontube pipeline',
        description='runs a pipeline server')

    parser.add_argument(
        'path',
        default='examples/simple.py',
        help='path to the python file containing the phase'
    )

    parser.add_argument(
        'name',
        help='the pipeline name'
    )

    parser.add_argument(
        '--sub-bind',
        help='a valid address in the form: tcp://<hostname>:<port>'
    )

    parser.add_argument(
        '--sub-connect',
        action='append',
        help='a valid address in the form: tcp://<hostname>:<port>'
    )

    parser.add_argument(
        '--pull-bind',
        default=None,
        help='a valid address in the form: tcp://<hostname>:<port>'
    )

    parser.add_argument(
        '--pull-connect',
        action='append',
        help='sets one or more connect addresses in which this pipeline should pull from'
    )
    parser.add_argument(
        '--concurrency',
        default=DEFAULT_CONCURRENCY,
        type=int,
        help='how many concurrent jobs to run at a time',
    )

    args = parser.parse_args(get_sub_parser_argv())
    bootstrap_conf_with_gevent(args, loglevel=logging.DEBUG)

    module_name = ".".join([
        "carbontube",
        "pipelines",
        sanitize_name(args.name).replace('-', '_'),
    ])

    module = imp.load_source(module_name, args.path)
    all_members = dict(
        map(lambda (name, member): (member.name, member),
            filter(lambda (name, member): (
                hasattr(member, 'name') and isinstance(member, type) and issubclass(member, Pipeline)
            ), inspect.getmembers(module)))
    )

    PipelineClass = all_members.get(args.name)

    if not PipelineClass:
        print "invalid job type \033[1;32m'{0}'\033[0m at \033[1;34m{1}\033[0m, but I found these \033[1;33m{2}\033[0m".format(args.name, args.path, ", ".join([x.name for x in all_members.values()]))
        raise SystemExit(1)

    server = PipelineClass(args.name, concurrency=args.concurrency)

    pull_connect_addresses = list(args.pull_connect or [])
    sub_connect_addresses = list(args.sub_connect or [])
    server.run(
        sub_connect_addresses=sub_connect_addresses,
        sub_bind_address=args.sub_bind,
        pull_bind_address=args.pull_bind,
        pull_connect_addresses=pull_connect_addresses,
    )


def execute_command_run_phase():
    """executes an instance of the phase server.

    :param ``--pub-bind``: address where the server will listen to announcements from Phases

    ::

      $ carbontube phase \\
          --pub-connect=tcp://127.0.0.1:6000
          # --push-connect=tcp://192.168.0.10:3000 # optional (can be used multiple times)
          # --pullf-connect=tcp://192.168.0.10:5050 # optional (can be used multiple times)
          # --pull-bind=tcp://0.0.0.0:5050    # optional (can be used only once)
    """

    parser = argparse.ArgumentParser(
        prog='carbontube phase',
        description='executes a phase server')

    parser.add_argument(
        'path',
        default='examples/simple.py',
        help='path to the python file containing the phase'
    )

    parser.add_argument(
        'job_type',
        help='the job type'
    )

    parser.add_argument(
        '--pub-connect',
        default='tcp://127.0.0.1:6000',
        help='a valid address in the form: tcp://<hostname>:<port>'
    )

    parser.add_argument(
        '--pull-bind',
        default='tcp://0.0.0.0',
        help='a valid address in the form: tcp://<hostname>[:<port>]'
    )
    parser.add_argument(
        '--pull-connect',
        action='append',
        help='sets one or more connect addresses in which this phase should pull from'
    )
    parser.add_argument(
        '--push-connect',
        action='append',
        help='sets one or more connect addresses in which this phase should push to'
    )

    parser.add_argument(
        '--concurrency',
        default=DEFAULT_CONCURRENCY,
        type=int,
        help='how many concurrent jobs to run at a time',
    )

    parser.add_argument(
        '--timeout',
        default=1,
        type=float,
        help='timeout',
    )

    args = parser.parse_args(get_sub_parser_argv())
    bootstrap_conf_with_gevent(args)

    pull_connect_addresses = list(args.pull_connect or [])
    push_connect_addresses = list(args.push_connect or [])

    module_name = ".".join([
        "carbontube",
        "phases",
        sanitize_name(args.job_type).replace('-', '_'),
    ])
    module = imp.load_source(module_name, args.path)
    all_members = dict(
        map(lambda (name, member): (member.job_type, member),
            filter(lambda (name, member): (
                hasattr(member, 'job_type') and isinstance(member, type) and issubclass(member, Phase)
            ), inspect.getmembers(module)))
    )

    PhaseClass = all_members.get(args.job_type)

    if not PhaseClass:
        print "invalid job type \033[1;32m'{0}'\033[0m at \033[1;34m{1}\033[0m, but I found these \033[1;33m{2}\033[0m".format(args.job_type, args.path, ", ".join([x.job_type for x in all_members.values()]))
        raise SystemExit(1)

    server = PhaseClass(
        pull_bind_address=args.pull_bind,
        pub_connect_address=args.pub_connect,
        concurrency=args.concurrency,
        push_connect_addresses=push_connect_addresses,
        pull_connect_addresses=pull_connect_addresses,
    )

    try:
        server.run()
    except KeyboardInterrupt:
        logging.info('exiting')


def execute_command_forwarder():
    """executes an instance of subscriber/publisher forwarder for scaling
    communications between multiple minions and masters.

    :param ``--subscriber``: the address where the forwarder subscriber where master servers can connect to.
    :param ``--publisher``: the address where the forwarder publisher where minion servers can connect to.

    ::

      $ carbontube forwarder \\
          --subscriber=tcp://0.0.0.0:6000 \\
          --publisher=tcp://0.0.0.0:6060 \\
          --subscriber-hwm=1000 \\
          --publisher-hwm=1000 \\

    """
    parser = argparse.ArgumentParser(
        prog='carbontube forwarder --subscriber=tcp://0.0.0.0:6000 --publisher=tcp://0.0.0.0:6060',
        description='runs a forwarder to broadcast events coming from minions')

    parser.add_argument(
        '--subscriber',
        default='tcp://0.0.0.0:6000',
        help=(
            'a valid ZeroMQ socket address where the Subscriber (SUB) will listen'
        )
    )
    parser.add_argument(
        '--publisher',
        default='tcp://0.0.0.0:6060',
        help=(
            'a valid ZeroMQ socket address where the Publisher (PUB) will listen'
        )
    )
    parser.add_argument(
        '--publisher-hwm',
        type=int,
        default=64,
        help=(
            'a hard limit on the maximum number messages that '
            'the forwarder should hold in memory before dropping them.'
            'If you start losing messages, then you need more forwarders. '
        )
    )
    parser.add_argument(
        '--subscriber-hwm',
        type=int,
        default=64,
        help=(
            'a hard limit on the maximum number messages that '
            'the forwarder should hold in memory before dropping them.'
            'If you start losing messages, then you need more forwarders. '
        )
    )

    args = parser.parse_args(get_sub_parser_argv())
    bootstrap_conf_with_gevent(args)

    device = Device(zmq.FORWARDER, zmq.SUB, zmq.PUB)

    device.bind_in(args.subscriber)
    device.bind_out(args.publisher)
    device.setsockopt_in(zmq.SUBSCRIBE, b'')
    if args.subscriber_hwm:
        device.setsockopt_in(zmq.RCVHWM, args.subscriber_hwm)

    if args.publisher_hwm:
        device.setsockopt_out(zmq.SNDHWM, args.publisher_hwm)

    print "carbontube forwarder started"
    print "date", datetime.utcnow().isoformat()
    print "subscriber", (getattr(args, 'subscriber'))
    print "publisher", (getattr(args, 'publisher'))
    device.start()


def execute_command_streamer():
    """executes an instance of pull/push streamer for scaling pipelines
    and/or phases


    :param ``--pull``: the address where the streamer pull where master servers can connect to.
    :param ``--push``: the address where the streamer push where minion servers can connect to.

    ::

      $ carbontube streamer \\
          --pull=tcp://0.0.0.0:5050 \\
          --push=tcp://0.0.0.0:6060 \\
          --pull-hwm=1000 \\
          --push-hwm=1000 \\

    """
    parser = argparse.ArgumentParser(
        prog='carbontube streamer --pull=tcp://0.0.0.0:6000 --push=tcp://0.0.0.0:6060',
        description='runs a streamer to broadcast events coming from minions')

    parser.add_argument(
        '--pull',
        default='tcp://0.0.0.0:6000',
        help=(
            'a valid ZeroMQ socket address where the Pull (SUB) will listen'
        )
    )
    parser.add_argument(
        '--push',
        default='tcp://0.0.0.0:6060',
        help=(
            'a valid ZeroMQ socket address where the Push (PUB) will listen'
        )
    )
    parser.add_argument(
        '--push-hwm',
        type=int,
        default=64,
        help=(
            'a hard limit on the maximum number messages that '
            'the streamer should hold in memory before dropping them.'
            'If you start losing messages, then you need more streamers. '
        )
    )
    parser.add_argument(
        '--pull-hwm',
        type=int,
        default=64,
        help=(
            'a hard limit on the maximum number messages that '
            'the streamer should hold in memory before dropping them.'
            'If you start losing messages, then you need more streamers. '
        )
    )

    args = parser.parse_args(get_sub_parser_argv())
    bootstrap_conf_with_gevent(args)

    device = Device(zmq.STREAMER, zmq.PULL, zmq.PUSH)

    device.bind_in(args.pull)
    device.bind_out(args.push)
    if args.pull_hwm:
        device.setsockopt_in(zmq.RCVHWM, args.pull_hwm)

    if args.push_hwm:
        device.setsockopt_out(zmq.SNDHWM, args.push_hwm)

    print "carbontube streamer started"
    print "date", datetime.utcnow().isoformat()
    print "pull", (getattr(args, 'pull'))
    print "push", (getattr(args, 'push'))
    device.start()


def execute_command_run_bundle():
    """executes a pipeline and all its phases in greenlets, good for
    quickly testing the full pipeline.

    ::

      $ carbontube bundle pipelines/example1.py "my-pipeline" --concurrency=32

    """

    parser = argparse.ArgumentParser(
        prog='carbontube pipeline',
        description='runs a pipeline server')

    parser.add_argument(
        'path',
        help='path to the python file containing the phase'
    )

    parser.add_argument(
        'name',
        help='the pipeline name'
    )
    parser.add_argument(
        '--sub-bind',
        default='tcp://127.0.0.1:6000',
        help='a valid address in the form: tcp://<hostname>:<port>'
    )
    parser.add_argument(
        '--pull-bind',
        default='tcp://127.0.0.1:7000',
        help='a valid address in the form: tcp://<hostname>:<port>'
    )

    parser.add_argument(
        '--concurrency',
        default=DEFAULT_CONCURRENCY,
        type=int,
        help='how many concurrent jobs to run at a time',
    )

    args = parser.parse_args(get_sub_parser_argv())
    bootstrap_conf_with_gevent(args, loglevel=logging.DEBUG)

    module_name = ".".join([
        "carbontube",
        "pipelines",
        sanitize_name(args.name).replace('-', '_'),
    ])

    module = imp.load_source(module_name, args.path)
    all_members = dict(
        map(lambda (name, member): (member.name, member),
            filter(lambda (name, member): (
                hasattr(member, 'name') and isinstance(member, type) and issubclass(member, Pipeline)
            ), inspect.getmembers(module)))
    )

    PipelineClass = all_members.get(args.name)

    if not PipelineClass:
        print "invalid job type \033[1;32m'{0}'\033[0m at \033[1;34m{1}\033[0m, but I found these \033[1;33m{2}\033[0m".format(args.name, args.path, ", ".join([x.name for x in all_members.values()]))
        raise SystemExit(1)

    server = PipelineClass(args.name, concurrency=args.concurrency)
    server.run_bundle(args.sub_bind, args.pull_bind)
