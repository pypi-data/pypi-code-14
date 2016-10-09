#!/usr/bin/env python
# coding: utf8

import argparse
import runner


def _build_args():
    parser = argparse.ArgumentParser(description='Usage by xlzd')
    parser.add_argument('cmd', nargs='?', type=str, help='start/stop/show')

    parser.add_argument('-r', '--range', type=str, help='show status, eg: 1475841137-1475927531')
    parser.add_argument('-o', '--output', type=str, help='output file path(default: terminal)')
    parser.add_argument('-f', '--format', type=str, help='output format(default: table)')

    return parser


def main():
    parser = _build_args()
    args = parser.parse_args()

    if args.cmd not in ('start', 'stop', 'show'):
        parser.print_help()
        exit(0)

    getattr(runner, args.cmd)()

if __name__ == '__main__':
    main()
