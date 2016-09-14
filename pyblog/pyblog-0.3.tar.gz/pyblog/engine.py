from . import utils
from datetime import datetime
import os, sys, jinja2

DEFAULT_CONFIG = """name: A PyBlog Blog
tagline: Demoing quick-and-dirty python blog generation
root_url: https://blog.com
"""

class Page:
    title           = u''
    content         = u''
    template        = None
    slug            = u''
    url             = u''
    date            = datetime.now()
    
    def __init__(self, dir, file_path):
        """Creates a generic page from a file"""
        parts = utils.file_get(dir, file_path).split('\n\n', 1)
        if len(parts) == 2:
            meta = utils.parse_headers(parts[0])
            self.content = parts[1]
            self.title = meta['title']
            if 'template' in meta:
                self.template = meta['template'] 
            if 'date' in meta:
                self.date = datetime.strptime(meta['date'], '%Y-%m-%d %H:%M:%S')
            else:
                self.date = utils.file_mtime(dir, file_path)
        else:
            self.content = parts[0]
            self.date = utils.file_mtime(dir, file_path)
    
    @staticmethod
    def make_post(blog, file):
        """Creates a post object"""
        post = Page(blog.posts_dir, file)
        post.slug = utils.slugify(post.title)
        post.url = post.date.strftime('%Y/')+post.slug+'.html'
        return post
    
    @staticmethod
    def make_page(blog, file):
        """Creates a page object"""
        page = Page(blog.pages_dir, file)
        page.slug = file
        page.url = file
        tpl = blog.env.from_string(page.content)
        page.content = tpl.render(blog=blog)
        return page
    
    def __repr__(self):
        return 'Blog.Page(%s)' % self.slug

class Blog:
    name            = u''
    root_url        = u''
    tagline         = u''
    in_dir          = u''
    pages_dur       = u''
    posts_dir       = u''
    templates_dir   = u''
    static_dir      = u''
    out_dir         = u''
    env             = None
    
    def __init__(self, in_dir, out_dir):
        """Creates the blog object from the config file"""
        data = utils.file_get(in_dir, 'config.txt')
        options = utils.parse_headers(data)
        
        self.name           = options['name']
        self.tagline        = options['tagline']
        self.root_url       = options['root_url']
        
        self.templates_dir  = os.path.join(in_dir, '_templates')
        self.static_dir     = os.path.join(in_dir, '_static')
        self.pages_dir      = os.path.join(in_dir, '_pages')
        self.posts_dir      = os.path.join(in_dir, '_posts')
        self.in_dir         = in_dir
        self.out_dir        = out_dir
        
        utils.dir_make(out_dir)
        utils.dir_copy(self.static_dir, out_dir)
        self.env = utils.create_jinja_env(self.templates_dir)
    
    def get_posts(self):
        """returns a list of all posts objects"""
        files = utils.file_list(self.posts_dir, '.txt')
        return sorted([Page.make_post(self, file) for file in files],
            key=lambda x: x.date, reverse=True)
    
    def get_pages(self):
        """returns a list of all pages objects"""
        files = utils.file_list(self.pages_dir)
        return sorted([Page.make_page(self, file) for file in files],
            key=lambda x: x.date, reverse=True)
    
    def write_html(self, post):
        if(post.template):
            template = self.env.get_template(post.template)
            utils.file_put(self.out_dir, post.url, template.render(blog=self, post=post))
        else:
            utils.file_put(self.out_dir, post.url, post.content)
        
    
    @staticmethod
    def dir_init(dir):
        utils.dir_make(os.path.join(dir, '_posts'))
        utils.dir_make(os.path.join(dir, '_pages'))
        utils.dir_make(os.path.join(dir, '_static'))
        utils.dir_make(os.path.join(dir, '_templates'))
        utils.file_put(dir, 'config.txt', DEFAULT_CONFIG)
        pass
    
    @staticmethod
    def compile(src, dist):
        """Used for command-line usage, compiles the blog"""
        engine = Blog(src, dist)
        for post in engine.get_posts():
            engine.write_html(post)
        for page in engine.get_pages():
            engine.write_html(page)
    
    def __repr__(self):
        return 'Blog.Engine(%s)' % root_url
        