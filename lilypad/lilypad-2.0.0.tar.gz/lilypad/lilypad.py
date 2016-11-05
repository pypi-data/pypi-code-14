"""Quick-and-dirty static site generator for Python 3 (exclusively)
using jinja & markdown.

This script generates the lillian.link static website from `_src`.

I really just made this for fun and I knew exactly
what I wanted in a static site generator:

  * `jinja2` for templates and pages (`_src/templates/`)
  * `markdown` for blog posts (`_src/markdown_blog/`), which can be
    categorized simply by organizing the markdown files into directories

How it works:
    Every jinja2 template (HTML file) in `_src/templates/pages/`
    will be rendered to the project's root (wherever lilypad is
    being executed from/current working directory). For the blog,
    the following jinja2 templates are required:

      * `src_/templates/lilypad/category-index.html
      * `src_/templates/lilypad/blog.html
      * `src_/templates/lilypad/blog-article.html

    The `_src/markdown_blog/` directory is scanned for markdown files
    recursively (`*.md`). The filename must fit the format
    `YYYY-MM-DD_some-title`.

    This post:

      _src/markdown_blog/rants/2016-11-05_i-really-love-halloween.md

    ...would belong to the `rants` category, and would be rendered to
    `blog/rants/2016-11-05_i-really-love-halloween.html`. The above
    post would have a timestamp of 2016-11-05.

Quickstart:
    Just modify some files in `_src` and then run this script!

      $ python lilypad.py

    If you want to test the site, just do this:

        $ python -m http.server 8000

    ... then open http://localhost/index.html in web browser.

"""

import sys
import os
sys.path.append(os.getcwd())
import datetime
import glob
from collections import namedtuple

import jinja2
from bs4 import BeautifulSoup
import markdown


jinja_env = jinja2.Environment(
    loader=jinja2.PackageLoader(
        '_src',
        'templates',
    )
)


class Post(object):
    """A blog post; make templating much easier.

    Constants:
        SUMMARY_CHARACTER_LIMIT (int): --
        TEMPLATE (str): jinja2 template to pull from the jinja2
            environment. This temple is used to render the post.
        MARKDOWN_SOURCE (str): --
        DATE_FORMAT (str): for strftime

    Attributes:
        href (str): Relative path to this article (html). Usable for
            both writing to local directory and as the href attribute
            of a link, in order to link to this post.
        category (str): Derived from the name of the directory
            containing this post.
        summary (str): A string summary (truncated) of the first
            paragraph of the content.
        content (BeautifulSoup): --
        timestamp (str): ---
        timestamp_as_int (int): --

    """

    SUMMARY_CHARACTER_LIMIT = 100
    TEMPLATE = 'lilypad/blog-article.html'
    MARKDOWN_SOURCE = os.path.join(
        '_src',
        'markdown_blog'
    )
    DATE_FORMAT = "%a, %d %b %Y"

    def __init__(self, file_path):
        """

        Arguments:
            file_path (str): Path to the markdown source file, which
                is a blog post.

        """

        self.category = self.get_category(file_path)
        self.content, self.title = self.get_html(file_path)
        self.summary = self.summarize(self.content)
        self.href = self.get_href(self.category, file_path)
        self.timestamp, self.timestamp_as_int = self.get_both_timestamps(file_path)

        if not os.path.exists('blog/' + self.category):
            os.makedirs('blog/' + self.category)

    @classmethod
    def get_category(cls, path_to_file):
        """Return the directory which contains path_to_file.

        Returns:
            str

        """

        directory_path = os.path.dirname(path_to_file)
        category = os.path.basename(directory_path)
        return category

    @classmethod
    def summarize(cls, soup):
        """Take BeautifulSoup and summarize the first paragraph.

        Returns:
            str:

        """

        first_paragraph = soup.find('p').get_text()

        if len(first_paragraph) > cls.SUMMARY_CHARACTER_LIMIT:
            return first_paragraph[:cls.SUMMARY_CHARACTER_LIMIT] + '&hellip;'
        else:
            return first_paragraph

    @staticmethod
    def get_href(category, file_path):
        """Path usable on both web server and for writing
        HTML locally.

        Arguments:
            category (str):
            file_path (str):

        """

        _, file_name_md = file_path.rsplit('/', 1)
        return os.path.join(
            'blog',
            category,
            os.path.splitext(file_name_md)[0],
            'index.html',
        )

    @classmethod
    def get_both_timestamps(cls, file_path):
        """Returns both the nice string/human-legible timestamp, as
        well as the int version for sorting.

        """

        timestamp = file_path.rsplit('/', 1)[-1].split('_', 1)[0]
        nice_timestamp = datetime.datetime.strptime(timestamp, '%Y-%m-%d').strftime(cls.DATE_FORMAT)

        return nice_timestamp, int(timestamp.replace('-', ''))

    @staticmethod
    def get_html(file_path):

        with open(file_path) as f:
            html_string = markdown.markdown(f.read())

        soup = BeautifulSoup(html_string, 'html.parser')
        title = soup.h1.extract().get_text()
        return soup, title

    def render(self):
        post_template = jinja_env.get_template(self.TEMPLATE)
        return post_template.render(post=self)


def main():
    """This is the part that the CLI activates!"""

    # Create the regular pages first
    for template_name in jinja_env.list_templates():

        if not template_name.startswith('pages/'):
            continue

        template = jinja_env.get_template(template_name)
        with open(os.path.basename(template_name), 'w') as f:
            f.write(template.render())

    # Create the blog by first creating all the individual
    # posts, building an index of those posts..
    list_of_all_posts_unsorted = []
    categorized_posts = {}
    search_path = os.path.join(Post.MARKDOWN_SOURCE, '**/*.md')
    for file_path in glob.iglob(search_path, recursive=True):

        # Create the post object and render/output
        post = Post(file_path)
        # create a directory for media belonging to post
        media_directory = os.path.split(os.path.splitext(post.href)[0])[0]
        if not os.path.exists(media_directory):
            os.makedirs(media_directory)
        with open(post.href, 'w') as f:
            f.write(post.render())

        # File by category and add to list of all posts
        list_of_all_posts_unsorted.append(post)
        if post.category not in categorized_posts:
            categorized_posts[post.category] = [post]
        else:
            categorized_posts[post.category].append(post)

    # create the category indexes
    category_template = jinja_env.get_template('lilypad/category-index.html')
    for category, posts in categorized_posts.items():
        path_to_category_index = os.path.join(
            'blog',
            category,
            'index.html',
        )
        with open(path_to_category_index, 'w') as f:
            f.write(category_template.render(category=category, posts=posts))

    # ... then sort said post list by their creation time
    sorted_list_of_all_posts = sorted(
        list_of_all_posts_unsorted,
        key=lambda x: x.timestamp_as_int,
        reverse=True,
    )

    # .. finally render the blog index
    template = jinja_env.get_template('lilypad/blog.html')  # XXX
    with open('blog.html', 'w') as f:
        f.write(template.render(posts=sorted_list_of_all_posts, categories=categorized_posts.keys()))
