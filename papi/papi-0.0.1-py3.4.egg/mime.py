import papi.fp as fp
from collections import namedtuple

MimeType = namedtuple('MimeType', ['major', 'minor', 'props'])

def parse_mime_type(mime_str):
    if isinstance(mime_str, tuple):
        # special case to initialize a mime type from an existing mime type
        # or arbitrary tuple
        major, minor, props = fp.take(3, mime_str + (None, None, None))
        return MimeType(major or "*", minor or "*", props or {})
    parts = mime_str.strip().split(";")
    base = (fp.head(parts) or "*/*").split("/", 1)
    major = (fp.head(base) or "*").strip()
    minor = (fp.nth(1, base) or "*").strip()
    props = dict(
            (
                (k.strip(), v.strip())
                for (k, v)
                in map(parse_pair, fp.tail(parts) or ())
            )
        )
    return MimeType(major or "*", minor or "*", props)

def parse_pair(s):
    k, v = tuple(fp.take(2, s.split('=',1) + ["", ""]))
    return k.strip(), v.strip()

def get_q(mime):
    return float(mime.props.get('q', '1.0'))

def parse_http_accept(accept_str, sort=False):
    items = list(map(parse_mime_type, accept_str.split(',')))
    if sort:
        items = sorted(items, key=fp.compose(lambda x: -x, get_q))
    return items

def match_mime(pattern, candidate, prop_keys=()):
    candidate = MimeType(*candidate)
    pattern = MimeType(*pattern)

    if pattern.major != "*" and pattern.major != candidate.major:
        return False

    if pattern.minor != "*" and pattern.minor != candidate.minor:
        return False

    for prop_key in prop_keys:
        pattern_prop = pattern.props.get(prop_key)
        candidate_prop = candidate.props.get(prop_key)
        if pattern_prop is not None and pattern_prop != candidate_prop:
            return False

    return True

def mime_str(m):
    base = "{0}/{1}".format(m.major, m.minor)
    if len(m.props) > 0:
        props_str = ";".join(("{0}={1}".format(k,v) for k,v in m.props.items()))
        return "{0};{1}".format(base, props_str)
    else:
        return base
