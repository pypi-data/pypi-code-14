#!/usr/bin/env python3
# Ducker - search with DuckDuckGo from the command line

# Copyright (C) 2016 Jorge Maldonado Ventura

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import argparse
import logging
import os
import webbrowser

PROGRAM_DESCRIPTION = 'lets you search with DuckDuckGo from the command line'

# Logging for debugging purposes
logging.basicConfig(format='[%(levelname)s] %(message)s')
logger = logging.getLogger()

# Parse command line args
parser = argparse.ArgumentParser(description=PROGRAM_DESCRIPTION)
parser.add_argument('search_str', metavar="search_str",
                    nargs='+', help='what you want to search')


def open_url(url):
    """Open an URL in the user's default web browser.
    Whether the browser's output (both stdout and stderr) are suppressed
    depends on the boolean attribute ``open_url.suppress_browser_output``.
    If the attribute is not set upon a call, set it to a default value,
    which means False if BROWSER is set to a known text-based browser --
    elinks, links, lynx or w3m; or True otherwise.
    """
    if not hasattr(open_url, 'suppress_browser_output'):
        open_url.suppress_browser_output = (os.getenv('BROWSER') not in
                                            ['elinks', 'links', 'lynx', 'w3m'])
    logger.debug('Opening %s', url)
    if open_url.suppress_browser_output:
        _stderr = os.dup(2)
        os.close(2)
        _stdout = os.dup(1)
        os.close(1)
        fd = os.open(os.devnull, os.O_RDWR)
        os.dup2(fd, 2)
        os.dup2(fd, 1)
    try:
        webbrowser.open(url)
    finally:
        if open_url.suppress_browser_output:
            os.close(fd)
            os.dup2(_stderr, 2)
            os.dup2(_stdout, 1)


def simple_search():
    args = parser.parse_args()

    for search_str in args.search_str:
        logger.debug('Searching %s', search_str)
        open_url('https://duckduckgo.com/?q={}&ia=web'.format(search_str))
