#!/usr/bin/env python
from __future__ import print_function
import argparse
import itertools
import os
import sys
import urllib2
import urlparse


__version__ = VERSION = 0.1


def links(m3u8_url):
    scheme, netloc, path, params, query, fragment = urlparse.urlparse(m3u8_url)

    try:
        response = urllib2.urlopen(m3u8_url)
    except Exception as exc:
        print("Problem when fetching the M3U file (%s)!" % exc)
        print("Exiting...")
        sys.exit(os.EX_IOERR)

    segment_names = (
        line.strip()
        for line in response.readlines()
        if line and not line.startswith("#")
    )

    segment_urls = (
        urlparse.urlunparse([scheme, netloc, segment_name, None, None, None])
        for segment_name in segment_names
    )

    return itertools.chain((m3u8_url, ), segment_urls)


def print_link_list(m3u8_url):
    map(print, links(m3u8_url))


def main():
    parser = argparse.ArgumentParser(description="M3U link list generator")
    parser.add_argument("--m3u", help="M3U URL", required=True)
    parser.add_argument('--version', action='version',
                        version='m3ull %s' % VERSION)
    args = parser.parse_args()
    print_link_list(args.m3u)


if __name__ == "__main__":
    main()
