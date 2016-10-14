"""
Custom Jinja filters
"""

from jinja2 import Markup
from . import markdown_ext
from . import utils
from flask import url_for
import humanize
import arrow
from mambo import init_app, get_config


def format_datetime(dt, format):
    return "" if not dt else arrow.get(dt).format(format)


def format_date_time(dt):
    f = get_config("DATE_TIME_FORMAT", "MM/DD/YYYY h:mm a")
    return format_datetime(dt, f)


def format_date(dt):
    f = get_config("DATE_FORMAT", "MM/DD/YYYY")
    return format_datetime(dt, f)


def nl2br(s):
    """
    {{ s | nl2br }}

    Convert newlines into <p> and <br />s.
    """
    if not isinstance(s, basestring):
        s = str(s)
    s = re.sub(r'\r\n|\r|\n', '\n', s)
    paragraphs = re.split('\n{2,}', s)
    paragraphs = ['<p>%s</p>' % p.strip().replace('\n', '<br />') for p in
                  paragraphs]
    return '\n\n'.join(paragraphs)


def oembed(url, class_=""):
    """
    Create OEmbed link

    {{ url | oembed }}
    :param url:
    :param class_:
    :return:
    """
    o = "<a href=\"{url}\" class=\"oembed {class_}\" ></a>".format(url=url, class_=class_)
    return Markup(o)


def img_src(url, class_="", responsive=True, lazy_load=False, id_=""):
    """
    Create an image src

    {{ xyz.jpg | img_src }}

    :param url:
    :param class_:
    :param responsive:
    :param lazy_load:
    :param id_:
    :return:
    """
    data_src = ""
    if responsive:
        class_ += " responsive"
    if lazy_load:
        data_src = url,
        # 1x1 image
        url = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNgYAAAAAMAASsJTYQAAAAASUVORK5CYII="
        class_ += " lazy"

    img = "<img src=\"{src}\" class=\"{class_}\" id=\"{id_}\" data-src={data_src}>"\
        .format(src=url, class_=class_, id_=id_, data_src=data_src)
    return Markup(img)


def static_url(url):
    """
    {{ url | static }}
    :param url:
    :return:
    """
    return url_for('static', filename=url)


FILTERS = {
    # slug
    "slug": utils.slugify,

    # Transform an int to comma
    "int_comma": humanize.intcomma,

    "strip_decimal": lambda d: d.split(".")[0],

    "bool_to_yes": lambda b: "Yes" if b else "No",

    "bool_to_int": lambda b: 1 if b else 0,

    # Return a markdown to HTML
    "markdown": lambda text: Markup(markdown_ext.html(text)),

    # Create a Table of Content of the Markdown
    "markdown_toc": markdown_ext.toc,

    "nl2br": nl2br,

    # Require the format to be passed
    "format_datetime": format_datetime,

    "date": format_date,

    "date_time": format_date_time,

    # Show the date ago: Today, yesterday, July 27 (without year in same year), July 15 2014
    "date_since": humanize.naturaldate,

    # To show the time ago: 3 min ago, 2 days ago, 1 year 7 days ago
    "time_since": humanize.naturaltime,

    "oembed": oembed,

    "img_src": img_src,

    "static": static_url
}


def jinja_helpers(app):
    app.jinja_env.filters.update(FILTERS)


init_app(jinja_helpers)