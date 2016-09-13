#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
     Virtualchain
     ~~~~~
     copyright: (c) 2014-2015 by Halfmoon Labs, Inc.
     copyright: (c) 2016 by Blockstack.org

     This file is part of Virtualchain

     Virtualchain is free software: you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation, either version 3 of the License, or
     (at your option) any later version.

     Virtualchain is distributed in the hope that it will be useful,
     but WITHOUT ANY WARRANTY; without even the implied warranty of
     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
     GNU General Public License for more details.
     You should have received a copy of the GNU General Public License
     along with Virtualchain.  If not, see <http://www.gnu.org/licenses/>.
"""


import os
import argparse
from ConfigParser import SafeConfigParser

DEBUG = False
if os.environ.get("BLOCKSTACK_DEBUG") == "1":
    DEBUG = True

TESTSET = False
IMPL = None             # class, package, or instance that implements the virtual chain state

""" virtualchain daemon configs
"""

RPC_TIMEOUT = 5  # seconds

MULTIPROCESS_RPC_RETRY = 10

REINDEX_FREQUENCY = 10  # in seconds

AVERAGE_MINUTES_PER_BLOCK = 10
DAYS_PER_YEAR = 365.2424
HOURS_PER_DAY = 24
MINUTES_PER_HOUR = 60
SECONDS_PER_MINUTE = 60
MINUTES_PER_YEAR = DAYS_PER_YEAR*HOURS_PER_DAY*MINUTES_PER_HOUR
SECONDS_PER_YEAR = int(round(MINUTES_PER_YEAR*SECONDS_PER_MINUTE))
BLOCKS_PER_YEAR = int(round(MINUTES_PER_YEAR/AVERAGE_MINUTES_PER_BLOCK))
EXPIRATION_PERIOD = BLOCKS_PER_YEAR*1
AVERAGE_BLOCKS_PER_HOUR = MINUTES_PER_HOUR/AVERAGE_MINUTES_PER_BLOCK

BLOCKS_CONSENSUS_HASH_IS_VALID = 4*AVERAGE_BLOCKS_PER_HOUR


def get_impl(impl):
    """
    Get the implementation--either
    the given one (if not None), or
    the globally-set one (if not None).
    Raise exception if both are None.
    """
    global IMPL
    if impl is not None:
        return impl

    elif IMPL is not None:
        return IMPL

    else:
        raise Exception("No virtualchain implementation set")


def get_first_block_id(impl=None):
    """
    facade to implementation's first block
    """
    impl = get_impl(impl)
    return impl.get_first_block_id()


def get_working_dir(impl=None):
    """
    Get the absolute path to the working directory.
    """

    if os.environ.has_key("VIRTUALCHAIN_WORKING_DIR"):
        return os.environ["VIRTUALCHAIN_WORKING_DIR"]

    impl = get_impl(impl)

    from os.path import expanduser
    home = expanduser("~")

    working_dir = None
    if hasattr(impl, "working_dir") and impl.working_dir is not None:
        working_dir = impl.working_dir

    else:
        working_dir = os.path.join(home, "." + impl.get_virtual_chain_name(testset=TESTSET))

    if not os.path.exists(working_dir):
        os.makedirs(working_dir)

    return working_dir


def get_config_filename(impl=None):
    """
    Get the absolute path to the config file.
    """
    impl = get_impl(impl)

    working_dir = get_working_dir(impl=impl)
    config_filename = impl.get_virtual_chain_name(testset=TESTSET) + ".ini"

    return os.path.join(working_dir, config_filename)


def get_db_filename(impl=None):
    """
    Get the absolute path to the last-block file.
    """
    impl = get_impl(impl)

    working_dir = get_working_dir(impl=impl)
    lastblock_filename = impl.get_virtual_chain_name(testset=TESTSET) + ".db"

    return os.path.join(working_dir, lastblock_filename)


def get_lastblock_filename(impl=None):
    """
    Get the absolute path to the last-block file.
    """
    impl = get_impl(impl)

    working_dir = get_working_dir(impl=impl)
    lastblock_filename = impl.get_virtual_chain_name(testset=TESTSET) + ".lastblock"

    return os.path.join(working_dir, lastblock_filename)


def get_snapshots_filename(impl=None):
    """
    Get the absolute path to the chain's consensus snapshots file.
    """
    impl = get_impl(impl)

    working_dir = get_working_dir(impl=impl)
    snapshots_filename = impl.get_virtual_chain_name(testset=TESTSET) + ".snapshots"

    return os.path.join(working_dir, snapshots_filename)


def configure_multiprocessing(bitcoind_opts, impl=None):
    """
    Given the set of bitcoind options (i.e. the location of the bitcoind server),
    come up with some good multiprocessing parameters.

    Return (number of processes, number of blocks per process)
    Return (None, None) if we could make no inferences from the bitcoind opts.
    """

    if bitcoind_opts is None:
        return (None, None)

    if bitcoind_opts.has_key("multiprocessing_num_procs") and bitcoind_opts.has_key("multiprocessing_num_blocks"):
        return bitcoind_opts["multiprocessing_num_procs"], bitcoind_opts["multiprocessing_num_blocks"]

    if bitcoind_opts.get("bitcoind_server", None) is None:
        return (None, None)

    if bitcoind_opts["bitcoind_server"] in ["localhost", "127.0.0.1", "::1"]:
        # running locally
        return (1, 10)

    else:
        # running remotely
        return (10, 1)


def get_bitcoind_config(config_file=None, impl=None):
    """
    Set bitcoind options globally.
    Call this before trying to talk to bitcoind.
    """

    loaded = False

    bitcoind_server = None
    bitcoind_port = None
    bitcoind_user = None
    bitcoind_passwd = None
    bitcoind_use_https = None
    bitcoind_timeout = None
    bitcoind_mock = None
    bitcoind_mock_save_file = None

    if config_file is not None:

        parser = SafeConfigParser()
        parser.read(config_file)

        if parser.has_section('bitcoind'):

            if parser.has_option('bitcoind', 'server'):
                bitcoind_server = parser.get('bitcoind', 'server')

            if parser.has_option('bitcoind', 'port'):
                bitcoind_port = int(parser.get('bitcoind', 'port'))

            if parser.has_option('bitcoind', 'user'):
                bitcoind_user = parser.get('bitcoind', 'user')

            if parser.has_option('bitcoind', 'passwd'):
                bitcoind_passwd = parser.get('bitcoind', 'passwd')

            if parser.has_option('bitcoind', 'use_https'):
                use_https = parser.get('bitcoind', 'use_https')
            else:
                use_https = 'no'

            if parser.has_option("bitcoind", "save_file"):
                bitcoind_mock_save_file = parser.get("bitcoind", "save_file")

            if parser.has_option('bitcoind', 'mock'):
                mock = parser.get('bitcoind', 'mock')
            else:
                mock = 'no'

            if parser.has_option('bitcoind', 'timeout'):
                bitcoind_timeout = float(parser.get('bitcoind', 'timeout'))

            if use_https.lower() in ["yes", "y", "true", "1", "on"]:
                bitcoind_use_https = True
            else:
                bitcoind_use_https = False

            if mock.lower() in ["yes", "y", "true", "1", "on"]:
                bitcoind_mock = True
            else:
                bitcoind_mock = False
            
            loaded = True

    if not loaded:

        bitcoind_server = 'bitcoin.blockstack.com'
        bitcoind_port = '8332'
        bitcoind_user = 'blockstack'
        bitcoind_passwd = 'blockstacksystem'
        bitcoind_use_https = False
        bitcoind_mock = False
        bitcoind_timeout = 300
        bitcoind_mock_save_file = None

    default_bitcoin_opts = {
        "bitcoind_user": bitcoind_user,
        "bitcoind_passwd": bitcoind_passwd,
        "bitcoind_server": bitcoind_server,
        "bitcoind_port": bitcoind_port,
        "bitcoind_use_https": bitcoind_use_https,
        "bitcoind_timeout": bitcoind_timeout,
        "bitcoind_mock": bitcoind_mock,
        "bitcoind_mock_save_file": bitcoind_mock_save_file
    }

    return default_bitcoin_opts


def parse_bitcoind_args(return_parser=False, parser=None, impl=None):
    """
     Get bitcoind command-line arguments.
     Optionally return the parser used to do so as well.
    """

    impl = get_impl(impl)

    opts = {}

    if parser is None:
        parser = argparse.ArgumentParser(description='%s version %s' % (impl.get_virtual_chain_name(testset=TESTSET), impl.get_virtual_chain_version()))

    parser.add_argument(
          '--bitcoind-server',
          help='the hostname or IP address of the bitcoind RPC server')
    parser.add_argument(
          '--bitcoind-port', type=int,
          help='the bitcoind RPC port to connect to')
    parser.add_argument(
          '--bitcoind-user',
          help='the username for bitcoind RPC server')
    parser.add_argument(
          '--bitcoind-passwd',
          help='the password for bitcoind RPC server')
    parser.add_argument(
          "--bitcoind-use-https", action='store_true',
          help='use HTTPS to connect to bitcoind')
    parser.add_argument(
          "--bitcoind-timeout", type=int,
          help='the number of seconds to wait before timing out a request')

    args, _ = parser.parse_known_args()

    # propagate options
    for (argname, config_name) in zip(["bitcoind_server", "bitcoind_port", "bitcoind_user", "bitcoind_passwd", "bitcoind_timeout"], \
                                      ["BITCOIND_SERVER", "BITCOIND_PORT", "BITCOIND_USER", "BITCOIND_PASSWD", "BITCOIND_TIMEOUT"]):

        if hasattr(args, argname) and getattr(args, argname) is not None:

            opts[argname] = getattr(args, argname)
            setattr(config, config_name, getattr(args, argname))

    if args.bitcoind_use_https:
        opts['bitcoind_use_https'] = True

    else:
        opts['bitcoind_use_https'] = False

    if return_parser:
        return opts, parser
    else:
        return opts


def get_implementation():
    """
    Get the globally-set implementation of the virtual chain state.
    """
    global IMPL
    return IMPL


def set_implementation(impl, testset):
    """
    Set the package, class, or bundle of methods
    that implements the virtual chain's core logic.
    This method must be called before anything else.
    """
    global TESTSET
    global IMPL

    IMPL = impl
    TESTSET = testset
