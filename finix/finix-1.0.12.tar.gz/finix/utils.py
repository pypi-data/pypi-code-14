from __future__ import unicode_literals
from . import wac_config


def to_uri(href):
    href = href.replace(wac_config.root_url, "") if href else ""
    return "/" + "/".join(filter(None, href.split("/")))
