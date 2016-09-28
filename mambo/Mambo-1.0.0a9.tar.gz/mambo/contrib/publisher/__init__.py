import functools
from mambo import register_package, get_config, abort, url_for, views, models, utils
from mambo.exceptions import AppError
import mambo.markdown_ext as md
import mambo.jinja_filters as jinja_filters
from jinja2 import Markup

register_package(__package__)

__version__ = "1.0.0"


def main(**kw):
    """
    Main entry of the package
    :param kw: **kwargs
    :return:
    """

    # Setup Jinja filters
    app = kw.get("app")

    @app.template_filter("publisher_title")
    def title(post):
        return post.title

    @app.template_filter("publisher_top_image")
    def top_image(post):
        return jinja_filters.img_src(post.top_image)

    @app.template_filter("publisher_featured_media")
    def featured_media(post):
        if post.featured_media_top:
            if post.featured_media_top == "embed" and post.featured_embed:
                return jinja_filters.oembed(post.featured_embed)
            elif post.featured_media_top == "image" and post.featured_image:
                return jinja_filters.img_src(post.featured_image)
        return ""

    @app.template_filter("publisher_body")
    def body(post, lazy_image=False):
        return Markup(md.html(post.content, lazy_images=lazy_image))

    @app.template_filter("publisher_published_date")
    def published_date(post):
        return jinja_filters.format_date(post.published_at)


def get_post(slug=None, id=None):
    """
    Return a published post by id or slug
    :param slug:
    :param id:
    :return: Post
    """
    return models.PublisherPost.get_published(slug=slug, id=id)


def query_posts(categories=[], types=[], tags=[], page=1, limit=10):
    """
    Return a paginated generator of posts by categories, types, tags.
    :param categories: list of categories
    :param types: list of types
    :param tags: list of tags
    :param page: int - the page
    :param limit: limit
    :return: generator
    """

    posts = models.PublisherPost.get_published(categories=categories,
                                               types=types,
                                               tags=tags)
    posts = posts.paginate(page=page, per_page=limit)
    return posts

