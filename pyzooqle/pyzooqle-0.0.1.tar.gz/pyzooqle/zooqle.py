#!/usr/bin/python

from __future__ import unicode_literals
import sys
import requests
from bs4 import BeautifulSoup
import re

try:
    # Python 3 and later
    from urllib.parse import quote_plus
except ImportError:
    # Python 2
    from urllib import quote_plus


class BASE(object):
    URL = 'https://zooqle.com'
    SEARCH = '/search?q={}'
    SORT = '&s={}'
    ORDER = '&sd={}'


class SORT(object):
    ADDED = 'dt'
    SIZE = 'sz'
    SEEDERS = 'ns'


class ORDER(object):
    ASCENDING = 'a'
    DESCENDING = 'd'


class Torrent(object):
    def __init__(self, title, size, seeds, leechers, magnet):
        self.title = title
        self.size = size
        self.seeds = seeds
        self.leechers = leechers
        self.magnet = magnet

    def __repr__(self):
        return _valid_encoding('<Torrent(title={title})>'.format(title=self.title))

    def __str__(self):
        return _valid_encoding(self.title)

    def __unicode__(self):
        return self.title

    def __bool__(self):
        return bool(self.title)

    def __nonzero__(self):
        return bool(self.title)


def _valid_encoding(text):
    if not text:
        return
    if sys.version_info > (3,):
        return text
    else:
        return unicode(text).encode('utf-8')


# Convert gb to mb and make into float
def _gb_to_mb(size_data):
    if size_data[-2:].lower() == 'gb':
        return float(size_data[:-3]) * 1024.0
    elif size_data[-2:].lower() == 'mb':
        return float(size_data[:-3])


def _parse_torrents(soup):
    try:
        trs = soup.find_all('tr')
    except AttributeError as e:
        return []

    torrents = []
    for tr in trs[1:]:
        try:
            title = tr.a.text
            size = _gb_to_mb(tr.find('div', {'class': 'progress-bar prog-blue prog-l'}).text)
            seed_leech_raw = tr.find('div', {'class': 'progress prog trans90'})['title']
            seeds = int(re.sub(',', '', seed_leech_raw.split('|')[0].split(':')[1].strip()))
            leechers = int(re.sub(',', '', seed_leech_raw.split('|')[1].split(':')[1].strip()))
            magnet = tr.find('ul').a['href']
            torrents.append(Torrent(title, size, seeds, leechers, magnet))
        except:
            continue

    return torrents


def search(query, sort=SORT.SEEDERS, order=ORDER.DESCENDING):
    '''
    Search https://zooqle.com

    Args:
        query (str)         -- Search term(s)
        sort (Optional)     -- SORT.ADDED | SORT.SIZE | SORT.SEEDERS
        order (Optional)    -- ORDER.ASCENDING | ORDER.DESCENDING

    Returns:
        (list) pyzooqle.Torrent objects
    '''
    headers = {'User-Agent' : "Magic Browser"}
    req_url = (BASE.URL + BASE.SEARCH.format(quote_plus(query)) + BASE.SORT.format(sort) + BASE.ORDER.format(order))
    s = requests.get(req_url, headers=headers)
    html = s.content
    soup = BeautifulSoup(html, 'html.parser')
    return _parse_torrents(soup)
