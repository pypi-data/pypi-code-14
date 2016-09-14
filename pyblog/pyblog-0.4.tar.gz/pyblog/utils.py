import markdown
import jinja2
import os
import re
from distutils import dir_util
from datetime import datetime

md = markdown.Markdown(extensions=[
    'markdown.extensions.fenced_code',
    'markdown.extensions.tables',
    'markdown.extensions.smarty',
	'markdown.extensions.codehilite(css_class=highlight, linenums=False)'
])

# Filesystem shortcuts

def dir_copy(src, dist):
    dir_util.copy_tree(src, dist)

def dir_make(path):
    if not os.path.exists(path):
        os.makedirs(path)

def file_get(dir, file_name):
    """Returns the UTF-8 decoded contents of a file"""
    with open(os.path.join(dir, file_name)) as f:
        return f.read().decode('utf-8')

def file_put(dir, file_name, contents):
    """Saves a utf-8 string to a file"""
    path = os.path.join(dir, file_name)
    dir_make(os.path.dirname(path))
    with open(path, 'w') as f:
        f.write(contents.encode('utf-8'))

def file_list(dir, ext=''):
    return [f for f in os.listdir(dir) if 
        os.path.isfile(os.path.join(dir, f)) and f.endswith(ext)]

def file_mtime(dir, file_name):
    datetime.fromtimestamp(os.path.getmtime(os.path.join(dir, file_name)))
        
# Blog utilities

def parse_headers(str):
    """Parses a HTTP-style headers"""
    headers = {}
    for line in str.split('\n'):
        key, value = line.split(': ', 1)
        headers[key] = value
    return headers

def create_jinja_env(tpl_path):
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(tpl_path))
    env.filters['markdown'] = markdown
    env.filters['shortdate'] = shortdate
    env.filters['longdate'] = longdate
    env.filters['rssdate'] = rssdate
    env.filters['slugify'] = slugify
    return env

# Filters, used for jinja

def slugify(text):
    """Creates a url-valid slug fro a string"""
    slug = text.encode('ascii', 'ignore').lower()
    slug = re.sub(r'[^a-z0-9]+', '-', slug).strip('-')
    slug = re.sub(r'[-]+', '-', slug)
    return slug

def markdown(text):
    """Markdownify a piece of text"""
    return jinja2.Markup(md.convert(text))

def shortdate(t):
    """Returns a british-formatted date without the year"""
    return t.strftime('%b %d')

def longdate(t):
    """Returns a british-formatted date with the year"""
    return t.strftime('%b %d, %Y')

def rssdate(t):
    """Returns a RSS-valid date without the year"""
    return t.strftime('%a, %d %b %Y %H:%M:%S %z')