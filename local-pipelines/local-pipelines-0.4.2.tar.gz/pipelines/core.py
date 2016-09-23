# vi:et:ts=4 sw=4 sts=4
#
# local-pipelines : run Bitbucket pipelines locally
# Copyright (C) 2016  Gary Kramlich <grim@reaperworld.com>
# Copyright (C) 2016  Sean Farley <sean@farley.io>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301  USA

from __future__ import print_function

import argparse
import os
import sys

import yaml

from pipelines import vcs, __version__
from pipelines.pipeline import Pipeline


def parse_args():
    parser = argparse.ArgumentParser(prog="pipelines")

    parser.add_argument(
        "-V", "--version",
        action="version",
        version="%(prog)s " + str(__version__),
    )

    parser.add_argument(
        "-f", "--pipeline",
        help="The filename of the pipeline file to use",
        metavar="FILENAME",
        default="bitbucket-pipelines.yml",
        dest="pipeline_filename",
    )

    parser.add_argument(
        "--env-file",
        help="The filename of the environment variables file to use",
        metavar="FILENAME",
        dest="env_filenames",
        default=[],
        action='append',
    )

    parser.add_argument(
        "-e", "--env",
        help="Set environment variable",
        metavar="ENVIRONMENT VARIABLE",
        dest="env",
        default=[],
        action='append',
    )

    parser.add_argument(
        "-n",
        help="Run a shell instead of the script in the container.  The " +
             "script can be run via /tmp/bitbucket-pipelines.sh.  This " +
             "will get weird if you're running more than one step.",
        dest="run_shell",
        action="store_true",
        default=False,
    )

    return parser.parse_args()


def _load_config(filename):
    try:
        with open(filename) as ifp:
            config = yaml.load(ifp.read())
            return os.path.dirname(filename), config
    except IOError:
        print("failed to open {}".format(filename))
        sys.exit(1)


def _split_env_var(line):
    kv = line.split("=", 1)
    k = kv[0].strip()
    v = None
    if len(kv) > 1:
        v = kv[1].strip()
    return k, v


def _parse_env_file(fn):
    env = {}

    with open(fn) as ifp:
        for line in ifp.readlines():
            line = line.strip()

            if len(line) > 0 and not line.startswith('#'):
                k, v = _split_env_var(line)
                env[k] = v

    return env


def _load_env(filenames):
    # let's maintain the order of variables in the file
    env = {}
    for fn in filenames:
        try:
            env.update(_parse_env_file(fn))
        except IOError:
            print("failed to open {}".format(fn))
            sys.exit(1)
    return env


def main():
    args = parse_args()

    path, config = _load_config(args.pipeline_filename)

    repo = vcs.repo(path)

    env = _load_env(args.env_filenames)

    # env vars passed through the command line take precedence
    for var in args.env:
        k, v = _split_env_var(var)
        env[k] = v

    pipeline = Pipeline(config, path, repo, args.run_shell, env)

    sys.exit(pipeline.run())
