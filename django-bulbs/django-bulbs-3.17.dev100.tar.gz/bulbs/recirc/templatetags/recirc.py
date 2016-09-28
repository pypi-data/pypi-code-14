import logging
import random

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.template import Context, Library
from django.template.loader import get_template

from bulbs.content.models import Content
from bulbs.promotion.models import PZone


logger = logging.getLogger(__name__)
register = Library()


@register.simple_tag
def end_of_article_video(**kwargs):
    '''
    templatetag that renders the end of article video recirc.
    '''
    inactive = kwargs.get("partial", False)
    if inactive:
        return ""

    try:
        queryset = PZone.objects.applied(name='end-of-article-videos')
    except ObjectDoesNotExist:
        queryset = None

    if not queryset:
        queryset = Content.search_objects.videos()

    try:
        queryset = queryset[:10]
        video = random.choice(queryset)
    except IndexError:
        logger.error('''Inline video recirc unable to retrieve video.''')
        return ""

    site_name = getattr(settings, "SITE_DISPLAY_NAME", None)
    recirc_text = "Watch Video"
    if site_name:
        recirc_text += " From " + site_name

    base_url = getattr(settings, "VIDEOHUB_BASE_URL", None)
    if base_url is None:
        return ""

    video_src = "{0}/video/{1}.json".format(base_url, video.videohub_ref.id)

    return get_template(
        "recirc/end_of_article.html"
    ).render(
        Context({
            'recirc_text': recirc_text.upper(),
            'video_src': video_src
        })
    )
