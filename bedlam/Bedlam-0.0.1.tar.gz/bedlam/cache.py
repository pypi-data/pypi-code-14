import re

from bedlam.errors import NotFound


_route_cache = {
    'get': [],
    'post': [],
    'put': [],
    'delete': [],
}


def register_route(method, uri_regex, handler):
    compiled = re.compile(uri_regex)
    _route_cache[method.lower()].append((compiled, handler,))


def map_route(method, uri):
    matches = _find_route_matches(method, uri)
    if not matches:
        raise NotFound

    match, handler = matches[0]

    groups = ()
    named_groups = match.groupdict()
    if not named_groups:
        groups = match.groups()
        named_groups = {}

    return handler, groups, named_groups


def _find_route_matches(method, uri):
    regexs_for_method = _route_cache[method.lower()]
    matches = []
    for regex, handler in regexs_for_method:
        match = regex.match(uri)
        if match:
            matches.append((match, handler,))
    return matches
