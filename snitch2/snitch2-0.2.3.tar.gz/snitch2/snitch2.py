"""Module contains core program logic
"""


from collections import deque

import requests

import parselink


def snitch(start_url, target_uri, max_crawl=1):
    """Return pages on starting domain that contains links to target URI"""
    visited = set()
    queue = deque()

    queue.append(start_url)

    pages_crawled = 0
    results = []

    while queue and pages_crawled < max_crawl:
        vertex = queue.popleft()
        
        visited.add(vertex)

        html_page = fetch_html(vertex)
        links = parselink.get_links(vertex, html_page)

        for link in links:
            # Ensure we do not add pages previously crawled to queue
            # and ensure we only crawl pages on starting domain
            if link['uri'] not in visited and link['kind'] == 'internal':
                queue.append(link['uri'])

            if parselink.contains(link['uri'], target_uri) and link['type'] == 'absolute':
                # We don't consider relative links on target domain to be guilty only
                # hard coded absolutes
                results.append({
                    "guilty_link": link,
                    "target_uri": target_uri,
                    "page_uri": vertex
                })

        pages_crawled += 1

    response = {
        "start_url": start_url,
        "target_uri": target_uri,
        "pages_crawled": pages_crawled,
        "guilty_total": len(results),
        "guilty_results": results  
    }

    return response


def fetch_html(uri):
    """Return HTML page as string"""
    uri = parselink.normalize_protocol(uri)
    return requests.get(uri).text


if __name__ == '__main__':
    print snitch('//joelcolucci.com', 'github.com', 2)