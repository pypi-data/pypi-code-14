"""Module contains core program logic
"""


from collections import deque
import json
import re
import urlparse

from bs4 import BeautifulSoup
import requests


def snitch(start_url, target_uri, max_crawl=1):
    """Return pages on starting domain that contains links to target URI"""
    visited = set()
    queue = deque()

    queue.append(start_url)

    origin_domain = strip_path(start_url)
    pages_crawled = 0
    results = []

    while queue and pages_crawled < max_crawl:
        vertex = queue.popleft()
        if vertex not in visited:
            visited.add(vertex)

            html_page = fetch_html(vertex)
            uris = extract_uris_from_html(html_page)

            for uri in uris:
                # Make sure we only crawl starting domain
                is_relative = is_relative_uri(uri)
                if contains(uri, origin_domain) or is_relative:
                    # Reassign to full_uri to ensure next condition does not prove True
                    # when we the target URI matches hard coded origin domain
                    if is_relative:
                        full_uri = '{}{}'.format(origin_domain, uri)
                    else:
                        full_uri = uri
                    queue.append(full_uri)

                if contains(uri, target_uri):
                    results.append({
                        "guilty_uri": uri,
                        "target_uri": target_uri,
                        "page_uri": vertex
                    })

            pages_crawled += 1

    response = {
        "start_url": start_url,
        "target_uri": target_uri,
        "pages_crawled": len(visited),
        "guilty_total": len(results),
        "guilty_results": results  
    }

    return json.dumps(response)


def crawl_page(start_url, target_uri):
    """Crawl single page looking for target_uri"""
    html_page = fetch_html(start_url)

    uris = extract_uris_from_html(html_page)
    results = []

    for uri in uris:
        if contains(uri, target_uri):
            results.append({
                "href": uri,
                "page_uri": start_url
            })

    result = {
        "start_url": start_url,
        "target_uri": target_uri,
        "guilty_total": len(results),
        "guilty_results": results
    }

    return result


def contains(str1, str2):
    """Return true if str1 contains str2"""
    try:
        result = str1.find(str2)
    except TypeError as e:
        return False # Handle if str2 is None
    except AttributeError as e:
        return False # Handle if str1 is None

    if result == -1:
        return False

    return True


def extract_uris_from_html(html_page):
    """Return list of anchor tags from page"""
    soup = BeautifulSoup(html_page, 'html.parser')
    results = []

    for link in soup.find_all('a'):
        href = link.get('href')
        results.append(href)

    return results


def is_relative_uri(uri):
    """Return True if uri is relative

    Expects normalized URI w/ scheme
    """
    domain = urlparse.urlparse(uri).netloc
    if not domain:
        return True

    return False


def strip_path(uri):
    domain = urlparse.urlparse(uri).netloc

    return normalize_uri(domain)


def normalize_uri(uri):
    """Return normalize URI (scheme, netloc, path)"""
    if not has_protocol(uri):
        if has_leading_forward_slashes(uri):
            uri = '{}{}'.format('http:', uri)
        else:    
            uri = '{}{}'.format('http://', uri)

    return uri


def fetch_html(uri):
    """Return HTML page as string"""
    uri = normalize_uri(uri)

    return requests.get(uri).text


def has_leading_forward_slashes(uri):
    """Return true if uri contains leading forward slashes"""
    start = uri[:2]

    if start == '//':
        return True
    
    return False


def has_protocol(uri):
    """Return True is uri has HTTP/HTTPS protocol"""
    regex = '(https?\:\/\/)'

    result = re.match(regex, uri)
    if result:
        return True

    return False


if __name__ == '__main__':
    print snitch('//joelcolucci.com', 'github.com', 2)