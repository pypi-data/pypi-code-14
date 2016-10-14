"""Module contains core program logic
"""


from collections import deque

import eventlet
from eventlet.green import urllib2
import requests

import parselink


def snitch(start_url, target_url, max_crawl=1, threaded=False):
    """Return pages on starting domain that contains links to target URI"""
    if threaded:
        response = _multi_thread_crawl(start_url, target_url, max_crawl)
    else:
        response = _single_thread_crawl(start_url, target_url, max_crawl)

    return response


def _multi_thread_crawl(start_url, target_url, max_crawl):
    """Return pages on starting domain that contains links to target URI"""
    """Recursively crawl starting from *start_url*.  Returns a set of
    urls that were found."""
    pool = eventlet.GreenPool()

    visited = set()
    queue = eventlet.Queue()
    results = []

    start_domain = parselink.get_domain(start_url)
    pages_crawled = 0

    queue.put(start_url)
    # keep looping if there are new urls, or workers that may produce more urls
    while True:
        while not queue.empty() and pages_crawled < max_crawl:
            url = queue.get()
            pages_crawled += 1

            # Ensure we only crawl pages on starting domain
            if url not in visited and parselink.contains(url, start_domain):
                visited.add(url)
                pool.spawn_n(_multi_thread_fetch, url, target_url, results, queue)

        pool.waitall()
        if queue.empty() or pages_crawled >= max_crawl:
            break

    response = {
        "pages_crawled": pages_crawled,
        "start_url": start_url,
        "target_url": target_url,
        "guilty_total": len(results),
        "guilty_results": results
    }

    return response


def _multi_thread_fetch(url, target_url, results, out_queue):
    """Fetch a url and push any urls found into a queue."""
    data = ''
    with eventlet.Timeout(5, False):
        normalized_url = parselink.normalize_protocol(url)
        data = urllib2.urlopen(normalized_url).read()

    links = parselink.get_links(url, data)

    for link in links:
        # Only add links on starting domain to queue to crawl
        # This is checked in the crawl function as well before dispatching green thread
        if link['kind'] == 'internal':
            out_queue.put(link['uri'])

        if parselink.contains(link['uri'], target_url) and link['type'] == 'absolute':
            # We don't consider relative links on target domain to be guilty only
            # hard coded absolutes
            results.append({
                "guilty_link": link,
                "target_url": target_url,
                "page_uri": url
            })


def _single_thread_crawl(start_url, target_url, max_crawl=1):
    """Return pages on starting domain that contains links to target URI"""
    visited = set()
    queue = deque()

    queue.append(start_url)

    pages_crawled = 0
    results = []

    while queue and pages_crawled < max_crawl:
        vertex = queue.popleft()

        visited.add(vertex)

        html_page = _fetch_html(vertex)
        links = parselink.get_links(vertex, html_page)

        for link in links:
            # Ensure we do not add pages previously crawled to queue
            # and ensure we only crawl pages on starting domain
            if link['uri'] not in visited and link['kind'] == 'internal':
                queue.append(link['uri'])

            if parselink.contains(link['uri'], target_url) and link['type'] == 'absolute':
                # We don't consider relative links on target domain to be guilty only
                # hard coded absolutes
                results.append({
                    "guilty_link": link,
                    "target_url": target_url,
                    "page_uri": vertex
                })

        pages_crawled += 1

    response = {
        "start_url": start_url,
        "target_url": target_url,
        "pages_crawled": pages_crawled,
        "guilty_total": len(results),
        "guilty_results": results
    }

    return response


def _fetch_html(uri):
    """Return HTML page as string"""
    uri = parselink.normalize_protocol(uri)
    return requests.get(uri).text


if __name__ == '__main__':
    print snitch('http://joelcolucci.com',
                 'github.com', 20, True)
