"""cloud_sptheme.ext.relbar_toc - addes TOC entry to relbar"""
import os.path
import logging; log = logging.getLogger(__name__)
from cloud_sptheme import __version__

def insert_toc(app, pagename, templatename, ctx, event_arg):
    if "rellinks" not in ctx:
        # e.g. json builder 'genindex' page
        return
    links = ctx['rellinks']

    #remove any existing toc (present on some pages)
    for idx,  elem in enumerate(links):
        if elem[3] == "toc":
            del links[idx]
            break

    #place toc right after "next" / "previous"
    idx = -1
    for idx, entry in enumerate(links):
        if entry[3] in ("next","previous"):
            break
    else:
        idx += 1

    #insert our toc entry
    # FIXME: there's probably a MUCH better / less broken way to do this
    if "pathto" in ctx:
        # normal html builder
        path = os.path.split(os.path.splitext(ctx['pathto']("contents"))[0])[1]
    else:
        # hardcode path for special "json" builder --
        # seems to always use docroot-relative paths
        path = "contents"
    links.insert(idx, (path, "Table Of Contents", "C", "toc"))

def setup(app):
    app.connect('html-page-context', insert_toc)

    # identifies the version of our extension
    return {'version': __version__}
