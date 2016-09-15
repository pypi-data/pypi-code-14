from django import template

register = template.Library()

from ..models import Post
from django.db.models import Count

from django.utils.safestring import mark_safe
import markdown


@register.simple_tag
def total_posts():
    return Post.published.count()

@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish').filter(post_type='post')[:count]
    return {'latest_posts': latest_posts}

@register.assignment_tag
def get_most_commented_posts(count=5):
    return Post.published.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]

@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))

@register.filter(name='get_range')
def get_range(value):
    return range(value)

@register.filter(name='substract')
def substract(value):
    return 10-value