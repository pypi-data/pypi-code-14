"""Module containing function for normalizing and parsing HTML anchor tags
link = {
    'type': ['internal', 'external', 'unknown'],
    'kind': ['relative', 'absolute'],
    'text': 'click here',
    'uri': 'https//joelcolucci.com',
    'domain': ''
}

"""


import re
import urlparse

from bs4 import BeautifulSoup


def get_links(page_uri, page_html):
    """Return list of link meta data for all links on page"""
    soup = BeautifulSoup(page_html, 'html.parser')

    domain = get_domain(page_uri)

    anchors = soup.find_all('a')
    results = []

    for anchor in anchors:
        href = anchor.get('href')
        
        if href:
            link = parse_link(href, domain)

            text = anchor.string
            link['text'] = text

            results.append(link)

    return results


def parse_link(href, domain):
    """Return dictionary of link attributes"""
    normalized_domain = get_domain(domain)

    href_type = get_href_type(href)

    kind = get_href_kind(href, domain)

    uri = get_href_uri(href, domain)

    return {
        'href': href,
        'type': href_type,
        'kind': kind,
        'uri': uri,
        'domain': normalized_domain
    }


def normalize_protocol(uri):
    """Return URI with full HTTP scheme"""
    if has_relative_protocol(uri):
        uri = '{}{}'.format('http:', uri)
    elif not has_http_protocol(uri):
        # Naively assume if URI does not have HTTP protocol then it has no protocol
        uri = '{}{}'.format('http://', uri)
    
    return uri

    
def has_relative_protocol(uri):
    """Return True if URI has relative protocol '//' """
    start = uri[:2]

    if start == '//':
        return True
    
    return False


def has_http_protocol(uri):
    """Return True if URI does not have HTTP protocol"""
    regex = '(https?\:\/\/)'

    result = re.match(regex, uri)
    if result:
        return True

    return False


def get_href_type(href):
    """Return type (relative, absolute) of href"""
    if is_relative_href(href):
        type = 'relative'
    else:
        type = 'absolute'

    return type


def is_relative_href(href):
    """Return True if href is relative else False"""

    _rule_re = re.compile(r'''
        (
            ^$              # empty string
            |
            ^\/($|[^\/ ]+)  # leading single '/'
        )
    ''', re.VERBOSE)

    result = re.match(_rule_re, href)

    if result or is_fragment(href):
        return True

    return False


def is_fragment(href):
    """Return True if href is a fragment else False"""
    is_fragment = False

    try:
        if href[0] == '#':
            is_fragment = True
    except IndexError:
        is_fragment = False

    return is_fragment


def get_href_kind(href, domain):
    """Return kind of href (internal or external)"""
    if is_internal_href(href, domain):
        kind = 'internal'
    else:
        kind = 'external'

    return kind


def is_internal_href(href, domain):
    """Return True if link is to an internal page else False"""
    if is_relative_href(href) or contains(href, domain):
        return True

    return False


def get_href_uri(href, domain):
    """Return full URI for href"""
    if is_relative_href(href):
        normalized_domain = normalize_protocol(domain)
        uri = '{}{}'.format(normalized_domain, href)
    else:
        uri = normalize_protocol(href)

    return uri


def get_domain(domain):
    """Return domain only (no protocol)"""
    normalized_domain = normalize_protocol(domain)

    url = urlparse.urlparse(normalized_domain)

    return url.netloc 


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


if __name__ == '__main__':
    pass